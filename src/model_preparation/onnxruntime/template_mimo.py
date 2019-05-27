import numpy as np
import torch
import torch.nn as nn
import argparse
from torchvision.models import resnet18


class MIMOModel(nn.Module):
    def __init__(self, max_vocab=5000, seq_len=60):
        super(MIMOModel, self).__init__()

        self.embedding = nn.Embedding(max_vocab, 128)
        self.conv_sequence = nn.Conv1d(128, 128, 3, padding=1)
        self.pool_sequence = nn.AvgPool1d(seq_len)

        self.image_forward = resnet18(pretrained=False, num_classes=128)

        self.features = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU()
        )
        self.output_layer = nn.Sequential(
            nn.Linear(128, 1000),
            nn.Softmax(dim=1)
        )

    def forward(self, input_text, input_image):
        # Extract text features
        x_text = self.embedding(input_text)  # (batch_size, seq_len, hidden_dim)
        x_text = torch.transpose(x_text, 2, 1)  # (batch_size, hidden_dim, seq_len)
        x_text = self.conv_sequence(x_text)
        text_features = self.pool_sequence(x_text)  # (batch_size, hidden_dim, 1)
        # text_features = torch.squeeze(x_text, dim=-1)  # (batch_size, hidden_dim)

        # Extract image features
        image_features = self.image_forward(input_image)

        # Concatenate features and feed into higher layer
        concat_features = torch.cat((text_features.view(-1, 128), image_features), dim=1)
        output_feature = self.features(concat_features)
        output_proba = self.output_layer(output_feature)
        return output_feature, output_proba


def main(args):
    model = MIMOModel(max_vocab=args.max_vocab, seq_len=args.seq_len)

    x_dummy_text = torch.LongTensor(np.random.randint(0, 4999, 60).reshape(1, -1))
    x_dummy_image = torch.FloatTensor(np.random.rand(1, 3, 224, 224).astype(np.float32))

    input_names = ['input_text', 'input_image']
    output_names = ['output_feature', 'output_proba']

    torch.onnx.export(model,
                      (x_dummy_text, x_dummy_image),
                      args.model_save_path,
                      export_params=True,
                      input_names=input_names,
                      output_names=output_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-vocab',
                        default=5000,
                        type=int)
    parser.add_argument('--seq-len',
                        default=60,
                        type=int)
    parser.add_argument('--model-save-path',
                        default='./data/mimo_model.onnx',
                        type=str,
                        help='Path to save the model.')
    args = parser.parse_args()
    main(args)

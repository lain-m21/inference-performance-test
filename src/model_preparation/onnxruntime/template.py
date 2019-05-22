import torch
import argparse
from cnn_finetune import make_model

from src.models.mobilenetv2 import MobileNetV2


def main(args):
    if args.model_name == 'mobilenetv2':
        model = MobileNetV2(num_classes=1000)
    else:
        model = make_model(args.model_name, num_classes=1000, pretrained=True)

    input_size = (1,) + tuple(model.original_model_info.input_size)
    x_dummy = torch.rand(input_size)

    input_names = ['input_0']
    output_names = ['output_0']
    torch.onnx.export(model,
                      x_dummy,
                      args.model_save_path,
                      export_params=True,
                      input_names=input_names,
                      output_names=output_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name',
                        default='densenet121',
                        type=str,
                        help='Model name to initialize in template')
    parser.add_argument('--model-save-path',
                        default='./data/model.onnx',
                        type=str,
                        help='Path to save the model.')
    args = parser.parse_args()
    main(args)

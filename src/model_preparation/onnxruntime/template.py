import torch
from cnn_finetune import make_model

from src.models.mobilenetv2 import MobileNetV2


def prepare_model(args):
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

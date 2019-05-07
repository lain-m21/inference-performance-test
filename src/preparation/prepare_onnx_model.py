import json
import logging
import argparse
from pathlib import Path
import torch
from cnn_finetune import make_model
from cnn_finetune.base import MODEL_REGISTRY

from src.models.mobilenetv2 import MobileNetV2


_logger = logging.getLogger(__name__)

SUPPORTED_MODELS = list(MODEL_REGISTRY.keys()) + ['mobilenetv2']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', type=str, default='densenet121', choices=SUPPORTED_MODELS)
    parser.add_argument('--num-classes', type=int, default=1000)
    parser.add_argument('--data-dir', type=str, default='./data')
    parser.add_argument('--save-name', type=str, default='densenet121_onnx')
    args = parser.parse_args()

    model_save_path = str(Path(args.data_dir).joinpath(args.save_name + '.onnx'))

    _logger.info('Prepare model.')
    if args.model_name == 'mobilenetv2':
        model = MobileNetV2(num_classes=args.num_classes)
    else:
        model = make_model(args.model_name, num_classes=args.num_classes, pretrained=True)

    input_size = (1,) + tuple(model.original_model_info.input_size)
    _logger.info('Create dummy input to the model with the shape {}.'.format(input_size))
    x_dummy = torch.rand(input_size)

    _logger.info('Export the model as a ONNX format to {}.'.format(model_save_path))
    torch.onnx.export(model, x_dummy, model_save_path, export_params=True)

    model_info = {
        'model_path': model_save_path,
        'input_size': input_size
    }
    model_info_path = Path(args.data_dir).joinpath(args.save_name + '_info.json')
    _logger.info('Save model info to {}.'.format(model_info_path))
    json.dump(model_info, model_info_path.open('w'))


if __name__ == '__main__':
    _logger.setLevel(logging.DEBUG)
    main()

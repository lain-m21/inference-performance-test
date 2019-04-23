import json
import logging
import argparse
from pathlib import Path
from tensorflow.python.keras.applications import *

_logger = logging.getLogger(__name__)
SUPPORTED_MODELS = [
    'vgg16', 'vgg19', 'resnet50', 'inception_v3', 'inceptionresnetv2', 'xception',
    'densenet121', 'densenet169', 'densenet201', 'nasnetlarge', 'nasnetmobile',
    'mobilenet', 'mobilenetv2'
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', type=str, default='densenet121', choices=SUPPORTED_MODELS)
    parser.add_argument('--num-classes', type=int, default=1000)
    parser.add_argument('--data-dir', type=str, default='./data')
    parser.add_argument('--save-name', type=str, default='densenet121_torch')
    args = parser.parse_args()

    model_save_path = str(Path(args.data_dir).joinpath(args.save_name + '.onnx'))

    _logger.info('Prepare model.')
    if args.model_name == 'vgg16':
        model = VGG16(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'vgg19':
        model = VGG19(weights=None, include_top=True, classes=args.num_classes)

    input_size = (1,) + tuple(model.original_model_info.input_size)
    _logger.info('Create dummy input to the model with the shape {}.'.format(input_size))
    x_dummy = torch.rand(input_size)

    _logger.info('Export the model as a ONNX format to {}.'.format(model_save_path))
    torch.onnx.export(model, x_dummy, model_save_path, export_params=True)

    model_info = {
        'model_path': model_save_path,
        'input_size': input_size
    }
    model_info_path = Path(args.data_dir).joinpath(args.save_name + '.json')
    _logger.info('Save model info to {}.'.format(model_info_path))
    json.dump(model_info, model_info_path.open('w'))


if __name__ == '__main__':
    _logger.setLevel(logging.DEBUG)
    main()

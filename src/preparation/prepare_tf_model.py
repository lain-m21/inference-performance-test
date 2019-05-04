import json
import logging
import argparse
from pathlib import Path
import tensorflow as tf
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
    parser.add_argument('--save-name', type=str, default='densenet121_tf')
    args = parser.parse_args()

    _logger.info('Prepare model.')
    if args.model_name == 'vgg16':
        model = VGG16(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'vgg19':
        model = VGG19(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'resnet50':
        model = ResNet50(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'inception_v3':
        model = InceptionV3(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'inceptionresnetv2':
        model = InceptionResNetV2(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'xception':
        model = Xception(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'densenet121':
        model = DenseNet121(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'densenet169':
        model = DenseNet169(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'densenet201':
        model = DenseNet201(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'nasnetlarge':
        model = NASNetLarge(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'nasnetmobile':
        model = NASNetMobile(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'mobilenet':
        model = MobileNet(weights=None, include_top=True, classes=args.num_classes)
    elif args.model_name == 'mobilenetv2':
        model = MobileNetV2(weights=None, include_top=True, classes=args.num_classes)
    else:
        raise ValueError('The given model is not supported.')

    input_size = (1,) + model.input_shape[1:]

    saved_model_path = str(Path(args.data_dir).joinpath(args.save_name))

    tf.keras.backend.set_learning_phase(0)

    _logger.info('Export the model as a saved_model.pb format to {}.'.format(saved_model_path))
    with tf.keras.backend.get_session() as sess:
        tf.saved_model.simple_save(
            sess,
            saved_model_path,
            inputs={'input_tensor': model.input},
            outputs={t.name: t for t in model.outputs}
        )

    model_info = {
        'model_path': saved_model_path,
        'input_size': input_size
    }
    model_info_path = Path(args.data_dir).joinpath(args.save_name + '_info.json')
    _logger.info('Save model info to {}.'.format(model_info_path))
    json.dump(model_info, model_info_path.open('w'))


if __name__ == '__main__':
    _logger.setLevel(logging.DEBUG)
    main()

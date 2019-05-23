import argparse
import tensorflow as tf
from tensorflow.python.keras.applications import *


def main(args):
    if args.model_name == 'vgg16':
        model = VGG16(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'vgg19':
        model = VGG19(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'resnet50':
        model = ResNet50(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'inception_v3':
        model = InceptionV3(weights=None, include_top=True, classes=1000, input_shape=(229, 229, 3))
    elif args.model_name == 'inceptionresnetv2':
        model = InceptionResNetV2(weights=None, include_top=True, classes=1000, input_shape=(229, 229, 3))
    elif args.model_name == 'xception':
        model = Xception(weights=None, include_top=True, classes=1000, input_shape=(229, 229, 3))
    elif args.model_name == 'densenet121':
        model = DenseNet121(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'densenet169':
        model = DenseNet169(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'densenet201':
        model = DenseNet201(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'nasnetlarge':
        model = NASNetLarge(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'nasnetmobile':
        model = NASNetMobile(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'mobilenet':
        model = MobileNet(weights=None, include_top=True, classes=1000)
    elif args.model_name == 'mobilenetv2':
        model = MobileNetV2(weights=None, include_top=True, classes=1000)
    else:
        raise ValueError('The given model is not supported.')

    tf.keras.backend.set_learning_phase(0)

    with tf.keras.backend.get_session() as sess:
        tf.saved_model.simple_save(
            sess,
            args.model_save_path,
            inputs={'input_0': model.input},
            outputs={'output_0': model.outputs[0]}
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name',
                        default='densenet121',
                        type=str,
                        help='Model name to initialize in template')
    parser.add_argument('--model-save-path',
                        default='./data/tf_model',
                        type=str,
                        help='Path to save the model.')
    args = parser.parse_args()
    main(args)

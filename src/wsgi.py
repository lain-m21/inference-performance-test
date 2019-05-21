import os
import argparse
import logging
import importlib


logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

serving_type = os.environ.get('SERVING_TYPE', 'onnxruntime')

module = 'src.{}_app'.format(serving_type)
app_module = importlib.import_module(module)

app = app_module.app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        default='0.0.0.0',
                        type=str,
                        help='host of predictor')
    parser.add_argument('--port',
                        default=9000,
                        type=int,
                        help='port of predictor')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()

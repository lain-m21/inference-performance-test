import argparse
import logging
import importlib


logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--framework',
                        default='sanic',
                        type='str',
                        help='REST framework, choose among flask, sanic, japronto, and falcon')
    parser.add_argument('--host',
                        default='0.0.0.0',
                        type=str,
                        help='host of predictor')
    parser.add_argument('--port',
                        default=8501,
                        type=int,
                        help='port of predictor')
    args = parser.parse_args()

    module = 'src.{}_app'.format(args.framework)
    app_module = importlib.import_module(module)

    app = app_module.app
    app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()

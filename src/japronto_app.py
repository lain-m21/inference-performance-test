import json
import logging
import argparse
from japronto import Application

from src.api import PredictionService

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


app = Application()
router = app.router
api = PredictionService()


def predict(request):
    data = request.json
    input_data = data['input']
    outputs = api.predict(input_data)
    return request.Response(text=json.dumps({'outputs': outputs.tolist()}))


def health(request):
    logger.info("[HEALTH] GET")
    return request.Response(text='')


router.add_route('/', health, method='GET')
router.add_route('/predict', predict, method='POST')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        default='0.0.0.0',
                        type=str,
                        help='host of predictor')
    parser.add_argument('--port',
                        default=8501,
                        type=int,
                        help='port of predictor')
    parser.add_argument('--debug',
                        action='store_true',
                        help='debug mode')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()

import json
import logging
import argparse
from sanic import Sanic
from sanic.response import json as sanic_json

from src.api import PredictionService

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


app = Sanic()
api = PredictionService()


@app.route('/predict', methods=['POST'])
async def predict(request):
    data = json.loads(request.json)
    input_data = data['input']
    outputs = api.predict(input_data)
    return sanic_json({'outputs': outputs.tolist()})


@app.route('/', methods=['GET'])
def health(request):
    logger.info("[HEALTH] GET")
    return sanic_json({'status': 'OK'})


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

import json
import logging
import argparse
from flask import Flask, request, jsonify

from src.api import PredictionService

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


app = Flask(__name__)
api = PredictionService()


@app.route('/predict', methods=['POST'])
def predict():
    print(request.data)
    print(request.get_json())
    # data = json.loads(request.data)
    data = request.get_json()
    input_data = data['input']
    outputs = api.predict(input_data)
    return jsonify({'outputs': outputs.tolist()})


@app.route('/', methods=['GET'])
def health():
    logger.info("[HEALTH] GET")
    return ''


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

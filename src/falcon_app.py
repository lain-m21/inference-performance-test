import json
import logging
import argparse
import falcon
import bjoern

from src.api import PredictionService


logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

api = PredictionService()


class PredictionResource:
    def on_post(self, req, resp):
        input_data = req.media.get('input')
        outputs = api.predict(input_data)

        resp.media = {'outputs': outputs.tolist()}
        resp.status = falcon.HTTP_200


class HealthResource:
    def on_get(self, req, resp):
        logger.info("[HEALTH] GET")
        resp.status = falcon.HTTP_200
        resp.body = ''


app = falcon.API()
predict_resource = PredictionResource()
health_resource = HealthResource()
app.add_route('/predict', predict_resource)
app.add_route('/', health_resource)


if __name__ == '__main__':
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

    bjoern.run(app, args.host, args.port)

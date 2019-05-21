import os
import logging
import importlib
from sanic import Sanic
from sanic.response import json as sanic_json
import grpc
from tensorflow_serving.apis import prediction_service_pb2_grpc


logger = logging.getLogger(__name__)


app = Sanic()
target = os.environ.get('TARGET', 'template')
endpoint = os.environ.get('ENDPOINT', 'localhost:8500')

channel = grpc.insecure_channel(endpoint)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

input_module_name = 'src.input_preparation.tensorflow.{}'.format(target)
output_module_name = 'src.output_decoding.tensorflow.{}'.format(target)
input_module = importlib.import_module(input_module_name)
output_module = importlib.import_module(output_module_name)


@app.route('/predict', methods=['POST'])
async def predict(request):
    predict_request = input_module.prepare_request(request)

    res = stub.Predict(predict_request, 30)
    outputs = output_module.decode_response(res)
    return sanic_json({'outputs': outputs})


@app.route('/', methods=['GET'])
async def health(request):
    logger.info("[HEALTH] GET")
    return sanic_json({'status': 'OK'})

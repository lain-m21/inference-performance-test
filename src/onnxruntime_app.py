import os
import logging
import importlib
import requests
from sanic import Sanic
from sanic.response import json as sanic_json
from src.utils import predict_pb2

logger = logging.getLogger(__name__)


app = Sanic()
target = os.environ.get('TARGET', 'template')
endpoint = os.environ.get('ENDPOINT', 'http://localhost:8001/v1/models/mymodel/versions/1:predict')

request_headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'application/octet-stream'
}

input_module_name = 'src.input_preparation.onnxruntime.{}'.format(target)
output_module_name = 'src.output_decoding.onnxruntime.{}'.format(target)
input_module = importlib.import_module(input_module_name)
output_module = importlib.import_module(output_module_name)


@app.route('/predict', methods=['POST'])
async def predict(request):
    predict_request = input_module.prepare_request(request)
    payload = predict_request.SerializeToString()

    res = requests.post(endpoint, headers=request_headers, data=payload)
    actual_result = predict_pb2.PredictResponse()
    actual_result.ParseFromString(res.content)
    outputs = output_module.decode_response(actual_result)
    return sanic_json({'outputs': outputs})


@app.route('/', methods=['GET'])
async def health(request):
    logger.info("[HEALTH] GET")
    return sanic_json({'status': 'OK'})

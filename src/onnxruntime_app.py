import os
import importlib
import requests
from sanic import Sanic
import numpy as np
import onnxruntime

from src.utils import onnx_predict_pb2, onnx_ml_pb2


app = Sanic()



@app.route('/predict', methods=['POST'])
async def predict(request):
    data = request.json
    input_data = data['input']
    outputs = api.predict(input_data)
    return sanic_json({'outputs': outputs.tolist()})


@app.route('/', methods=['GET'])
async def health(request):
    logger.info("[HEALTH] GET")
    return sanic_json({'status': 'OK'})

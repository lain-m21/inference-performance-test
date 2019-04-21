import os
import json
import numpy as np

from src.servables import Caffe2Predictor, ONNXRuntimePredictor, PyTorchPredictor


class PredictionService:
    def __init__(self):
        servable_type = os.environ.get('SERVABLE_TYPE')
        model_info_path = os.environ.get('MODEL_INFO_PATH')

        model_info = json.load(open(model_info_path, 'r'))
        model_path = model_info['model_path']
        input_size = model_info['input_size']

        if servable_type == 'pytorch':
            self.predictor = PyTorchPredictor(model_path, input_size)
        elif servable_type == 'caffe2':
            self.predictor = Caffe2Predictor(model_path, input_size)
        elif servable_type == 'onnxruntime':
            self.predictor = ONNXRuntimePredictor(model_path, input_size)
        else:
            raise ValueError('The given servable type is not supported.')

    def predict(self, input_data: list) -> np.ndarray:
        input_array = np.array(input_data, dtype=np.float32)
        outputs = self.predictor.predict(input_array)
        return outputs

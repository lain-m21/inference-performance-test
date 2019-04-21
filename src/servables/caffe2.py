import numpy as np
import onnx
import caffe2.python.onnx.backend as onnx_caffe2_backend


class Caffe2Predictor:
    def __init__(self, model_path: str, input_size: tuple = (1, 3, 224, 224)):
        model_onnx = onnx.load(model_path)
        self.model = onnx_caffe2_backend.prepare(model_onnx)
        self.input_name = model_onnx.graph.input[0].name
        self.input_size = input_size

    def predict(self, input_array: np.ndarray):
        assert input_array.shape == self.input_size
        input_array = input_array.astype(np.float32)
        outputs = self.model.run({self.input_name: input_array})[0]
        return outputs

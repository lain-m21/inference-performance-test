import numpy as np
import onnxruntime


class ONNXRuntimePredictor:
    def __init__(self, model_path: str, input_size: tuple = (1, 3, 224, 224)):
        self.model = onnxruntime.InferenceSession(model_path)
        self.input_name = self.model.get_inputs()[0].name
        self.label_name = self.model.get_outputs()[0].name
        self.input_size = input_size

    def predict(self, input_array: np.ndarray) -> np.ndarray:
        assert input_array.shape == self.input_size
        input_array = input_array.astype(np.float32)
        outputs = self.model.run([self.label_name], {self.input_name: input_array})[0]
        return outputs

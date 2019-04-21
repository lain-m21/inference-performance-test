import numpy as np
import torch


class PyTorchPredictor:
    def __init__(self, model_path: str, input_size: tuple = (1, 3, 224, 224)):
        self.model = torch.load(model_path)
        self.model.eval()
        self.input_size = input_size

    def predict(self, input_array: np.ndarray):
        assert input_array.shape == self.input_size
        input_array = input_array.astype(np.float32)
        input_tensor = torch.FloatTensor(input_array)
        output_tensor = self.model(input_tensor)
        outputs = output_tensor.numpy()
        return outputs

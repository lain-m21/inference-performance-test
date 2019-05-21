from typing import Union
import numpy as np
from src.utils import predict_pb2


def decode_response(res: predict_pb2.PredictResponse) -> Union[int, float, str, list, dict]:
    actual_result = predict_pb2.PredictResponse()
    actual_result.ParseFromString(res.content)
    outputs = np.frombuffer(actual_result.outputs['output_0'].raw_data, dtype=np.float32).tolist()
    return outputs

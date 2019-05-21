from typing import Union
from tensorflow_serving.apis import predict_pb2


def decode_response(res: predict_pb2.PredictResponse) -> Union[int, float, str, list, dict]:
    outputs = list(res.outputs['output_0'].float_val)
    return outputs

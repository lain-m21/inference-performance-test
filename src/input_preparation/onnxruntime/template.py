import numpy as np
from onnx import numpy_helper
from sanic.request import Request

from src.utils import predict_pb2, onnx_ml_pb2


def prepare_request(request: Request) -> predict_pb2.PredictRequest:
    """
    In your input preparation module, you are required to implement this method.
    You can specify whatever parameters in the request payload to the frontend sanic app to pass them to this method.
    The output of this method is predict_pb2.PredictRequest object. To prepare the object, you need to provide:

    - Inputs with valid names and corresponding tensor protos
    - Output filters with valid names

    You can refer to this template implementation to prepare your own request to the serving.
    You can also use a MIMO (Multi-Input, Multi-Output) model.

    :param request: sanic.request.Request
    :return: predict_pb2.PredictRequest
    """

    # Prepare input tensor proto from raw numpy array
    raw = np.random.rand(*request.json['input_size']).astype(np.float32)  # (1, 224, 224, 3) or (1, 299, 299, 3)
    tensor_proto = numpy_helper.from_array(raw)  # actually faster than manually initialize onnx_ml_pb2.TensorProto
    t = onnx_ml_pb2.TensorProto()
    t.ParseFromString(tensor_proto.SerializeToString())

    # Initialize PredictRequest instance
    predict_request = predict_pb2.PredictRequest()

    # Set the input tensor proto with a certain input name specified when saving
    predict_request.inputs['input_0'].CopyFrom(t)

    # Set an output filter with a certain output name specified when saving
    predict_request.output_filter.append('output_0')

    return predict_request

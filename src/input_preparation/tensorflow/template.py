import numpy as np
from sanic.request import Request
from tensorflow.contrib.util import make_tensor_proto

from tensorflow_serving.apis import predict_pb2


def prepare_request(request: Request) -> predict_pb2.PredictRequest:
    """
    In your input preparation module, you are required to implement this method.
    You can specify whatever parameters in the request payload to the frontend sanic app to pass them to this method.
    The output of this method is predict_pb2.PredictRequest object. To prepare the object, you need to provide:

    - Inputs with valid names and corresponding tensor protos
    - Model name with a directory name under which the saved_model.pb is saved

    You can refer to this template implementation to prepare your own request to the serving.
    You can also use a MIMO (Multi-Input, Multi-Output) model.

    :param request: sanic.request.Request
    :return: predict_pb2.PredictRequest
    """

    # Prepare input tensor proto from raw numpy array
    raw = np.random.rand(*request.json['input_size']).astype(np.float32)  # (224, 224, 3) or (299, 299, 3)
    tensor = make_tensor_proto(raw, shape=[1] + list(raw.shape))

    # Initialize PredictRequest instance
    predict_request = predict_pb2.PredictRequest()

    # Set the model name with a certain model name specified when saving
    predict_request.model_spec.name = 'densenet121_tf'
    predict_request.model_spec.signature_name = 'serving_default'  # this is default and you don't need to change

    # Set the input tensor proto with a certain input name specified when saving
    predict_request.inputs['input_0'].CopyFrom(tensor)

    return predict_request

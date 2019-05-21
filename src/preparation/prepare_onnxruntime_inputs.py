import json
import logging
import argparse
from pathlib import Path
import numpy as np
import onnxruntime
from onnx import numpy_helper

from src.utils import predict_pb2, onnx_ml_pb2


_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, default='./data')
    parser.add_argument('--model-info-path', type=str, default='densenet121_onnx_info.json')
    parser.add_argument('--save-path', type=str, default='densenet121_onnxruntime_payload.pb')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    _logger.info('Load model info from {}'.format(args.model_info_path))
    model_info = json.load(data_dir.joinpath(args.model_info_path).open('r'))

    model = onnxruntime.InferenceSession(model_info['model_path'])
    input_name = model.get_inputs()[0].name
    output_name = model.get_outputs()[0].name

    input_size = model_info['input_size']
    _logger.info('Generate inputs with size: {}'.format(input_size))
    input_tensor = np.random.rand(*input_size).astype(np.float32)
    d = numpy_helper.from_array(input_tensor)
    t = onnx_ml_pb2.TensorProto()
    t.ParseFromString(d.SerializeToString())

    predict_request = predict_pb2.PredictRequest()
    predict_request.inputs[input_name].CopyFrom(t)
    predict_request.output_filter.append(output_name)

    payload = predict_request.SerializeToString()

    _logger.info('Save the generated inputs as a payload for the saved onnx model into {}'.format(args.save_path))
    with data_dir.joinpath(args.save_path).open('wb') as f:
        f.write(payload)


if __name__ == '__main__':
    _logger.setLevel(logging.DEBUG)
    main()

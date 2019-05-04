import json
import logging
import argparse
from pathlib import Path
import numpy as np


_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str, default='./data')
    parser.add_argument('--model-info-path', type=str, default='densenet121_onnx_info.json')
    parser.add_argument('--save-path', type=str, default='densenet121_onnx_payload.json')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    _logger.info('Load model info from {}'.format(args.model_info_path))
    model_info = json.load(data_dir.joinpath(args.model_info_path).open('r'))

    input_size = model_info['input_size']
    _logger.info('Generate inputs with size: {}'.format(input_size))
    input_tensor = np.random.rand(input_size).astype(np.float32)
    payload = {'input': input_tensor.tolist()}

    _logger.info('Save the generated inputs as a payload for the saved onnx model into {}'.format(args.save_path))
    json.dump(payload, data_dir.joinpath(args.save_path).open('w'))


if __name__ == '__main__':
    _logger.setLevel(logging.DEBUG)
    main()

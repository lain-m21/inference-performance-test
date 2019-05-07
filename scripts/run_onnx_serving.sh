#!/bin/bash

# Ex: ./scripts/run_onnx_serving.sh sanic onnxruntime densenet121_onnx_info.json 18501

FRAMEWORK=$1
SERVABLE_TYPE=$2
MODEL_INFO_PATH=$3
REST_PORT_TUNNEL=$4
CONTAINER_NAME=${5:-onnx_serving}

ONNX_SERVING_IMAGE="tmp/onnx-serving:0.0.1"
DATA_DIR="/workspace/data"

docker run -d -p ${REST_PORT_TUNNEL}:8501 --rm -n ${CONTAINER_NAME}\
    -v $(pwd)/data:${DATA_DIR} \
    -e MODEL_INFO_PATH=${DATA_DIR}/${MODEL_INFO_PATH} \
    -e SERVABLE_TYPE=${SERVABLE_TYPE} \
    -e FRAMEWORK=${FRAMEWORK} \
    -t ${ONNX_SERVING_IMAGE}

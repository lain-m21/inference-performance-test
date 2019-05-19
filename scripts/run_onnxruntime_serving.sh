#!/bin/bash

# Ex: ./scripts/run_onnxruntime_serving_optimized.sh densenet121 8501

ONNXRUNTIME_SERVING_IMAGE="tmp/onnxruntime-serving:0.0.1"

SAVED_MODEL_NAME=$1
REST_PORT_TUNNEL=$2
NUM_HTTP_THREADS=${3:-$(nproc)}
CONTAINER_NAME=${4:-onnxruntime_serving}

docker run -d -p ${REST_PORT_TUNNEL}:8001 --rm --name ${CONTAINER_NAME} \
    -v $(pwd)/data:/models \
    -e MODEL_PATH=${SAVED_MODEL_NAME}.onnx -e NUM_HTTP_THREADS=${NUM_HTTP_THREADS}\
    -t ${ONNXRUNTIME_SERVING_IMAGE}
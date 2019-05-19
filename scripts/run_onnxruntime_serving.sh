#!/bin/bash

# Ex: ./scripts/run_onnxruntime_serving_optimized.sh densenet121 8501

ONNXRUNTIME_SERVING_IMAGE="tmp/onnxruntime-serving:0.0.1"

SAVED_MODEL_NAME=$1
REST_PORT_TUNNEL=$2
CONTAINER_NAME=${3:-onnxruntime_serving}

docker run -d -p ${REST_PORT_TUNNEL}:8001 --rm --name ${CONTAINER_NAME} \
    -v $(pwd)/data/${SAVED_MODEL_NAME}:/models/${SAVED_MODEL_NAME} -e MODEL_NAME=${SAVED_MODEL_NAME} \
    -t ${ONNXRUNTIME_SERVING_IMAGE}
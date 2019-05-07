#!/bin/bash

# Ex: ./scripts/run_tf_serving.sh densenet121_tf 8500 8501

TF_SERVING_IMAGE="tensorflow/serving:latest"
SAVED_MODEL_NAME=$1
GRPC_PORT_TUNNEL=$2
REST_PORT_TUNNEL=$3

docker run -d -p ${GRPC_PORT_TUNNEL}:8500 -p ${REST_PORT_TUNNEL}:8501 --rm \
    -v $(pwd)/data/${SAVED_MODEL_NAME}:/models/${SAVED_MODEL_NAME} -e MODEL_NAME=${SAVED_MODEL_NAME} \
    -t ${TF_SERVING_IMAGE}
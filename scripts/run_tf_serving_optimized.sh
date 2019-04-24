#!/bin/bash

TF_SERVING_IMAGE="tmp/tensorflow-serving-devel:0.0.1"
SAVED_MODEL_NAME=$1
GRPC_PORT_TUNNEL=$2
REST_PORT_TUNNEL=$3

docker run -d -p ${GRPC_PORT_TUNNEL}:8500 -p ${REST_PORT_TUNNEL}:8501 \
    -v $(pwd)/data/${SAVED_MODEL_NAME}:/models/${SAVED_MODEL_NAME} -e MODEL_NAME=${SAVED_MODEL_NAME} \
    -t ${TF_SERVING_IMAGE}
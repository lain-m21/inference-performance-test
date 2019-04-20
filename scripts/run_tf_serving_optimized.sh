#!/bin/bash

TF_SERVING_IMAGE="tmp/tensorflow-serving-devel:0.0.1"
SAVED_MODEL_PATH=$1
SERVING_MODEL_NAME=$2
GRPC_PORT_TUNNEL=$3
REST_PORT_TUNNEL=$4
NUM_THREADS=$5

docker run -d -p ${GRPC_PORT_TUNNEL}:8500 -p ${REST_PORT_TUNNEL}:8501 \
    -v $(pwd)/data/${SAVED_MODEL_PATH}:/models/${SAVED_MODEL_PATH} -e MODEL_NAME=${SERVING_MODEL_NAME} \
    -t ${TF_SERVING_IMAGE} \
    --tensorflow_intra_op_parallelism=${NUM_THREADS} \
    --tensorflow_inter_op_parallelism=${NUM_THREADS}
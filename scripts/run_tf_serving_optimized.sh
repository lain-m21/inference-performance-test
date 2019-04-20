#!/bin/bash

TF_SERVING_IMAGE="tmp/tensorflow-serving-devel:0.0.1"
SAVED_MODEL_PATH=$1
SERVING_MODEL_NAME=$2
NUM_THREADS=$3

docker run -d -p 9000:8500 \
    -v $(pwd)/data/${SAVED_MODEL_PATH}:/models/${SAVED_MODEL_PATH} -e MODEL_NAME=${SERVING_MODEL_NAME} \
    -t ${TF_SERVING_IMAGE} \
    --tensorflow_intra_op_parallelism=${NUM_THREADS} \
    --tensorflow_inter_op_parallelism=${NUM_THREADS}
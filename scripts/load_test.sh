#!/bin/bash

# Ex: ./scripts/load_test.sh tensorflow sanic densenet121_tf densenet121 8501 ./data/densenet121_tf_payload.json 10 5

SERVING_TYPE=$1
FRAMEWORK=$2
MODEL_NAME=$3
MODEL=$4
PORT=$5
PAYLOAD=$6
RATE=$7
DURATION=$8

if [[ ${SERVING_TYPE} == "tensorflow" ]]; then
    DIR="tensorflow"
    WATCH="tensorflow_model_server"
else
    DIR="${SERVING_TYPE}_${FRAMEWORK}"
    WATCH="python"
fi

VEGETA_DIR=./data/results/${MODEL}/${DIR}
METRICS_DIR=./data/metrics/${MODEL}/${DIR}

mkdir -p ${VEGETA_DIR}
mkdir -p ${METRICS_DIR}

OUTPUT_VEGETA="${VEGETA_DIR}/result_rate${RATE}_duration${DURATION}_cpu$(nproc)"
OUTPUT_METRICS="${METRICS_DIR}/metrics_rate${RATE}_duration${DURATION}_cpu$(nproc).npy"

python -m src.get_metrics --watch ${WATCH} --save-path ${OUTPUT_METRICS} &
./scripts/vegeta_attack.sh ${SERVING_TYPE} ${MODEL_NAME} ${PORT} ${PAYLOAD} ${RATE} ${DURATION} ${OUTPUT_VEGETA}
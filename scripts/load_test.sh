#!/bin/bash

SERVING_TYPE=$1
MODEL_NAME=$2
MODEL=$3
PORT=$4
PAYLOAD=$5
RATE=$6
DURATION=$7

if [[ ${SERVING_TYPE} == "tensorflow" ]]; then
    PREFIX="tf"
    WATCH="tensorflow_model_server"
else
    PREFIX="onnx"
    WATCH="python"
fi

OUTPUT_VEGETA="./data/result_${MODEL}_${PREFIX}_${RATE}_${DURATION}.bin"
OUTPUT_METRICS="./data/metrics_${MODEL}_${PREFIX}_${RATE}_${DURATION}.npy"

python -m src.get_metrics --watch ${WATCH} --save-path ${OUTPUT_METRICS}
./scripts/vegeta_attack ${SERVING_TYPE} ${MODEL_NAME} ${PORT} ${PAYLOAD} ${RATE} ${DURATION} ${OUTPUT_VEGETA}
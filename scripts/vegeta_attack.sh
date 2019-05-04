#!/bin/bash

# Ex: ./scripts/vegeta_attack.sh 10 5 ./tools/target_onnx.txt ./data/vegeta_result_onnx.bin

RATE=$1
DURATION=$2
TARGET=${3:-tools/target.txt}
OUTPUT=${4:-data/vegeta_result.bin}

echo "Vegeta attack - rate = ${RATE}, duration = ${DURATION}, target = ${TARGET}, output = ${OUTPUT}"

vegeta attack -rate=${RATE} -duration=${DURATION}s -targets=${TARGET} > ${OUTPUT}
cat ${OUTPUT} | vegeta report
cat ${OUTPUT} | vegeta report -type='hist[0,100ms,200ms,300ms,400ms,500ms,1s,2s,3s,4s,5s]'
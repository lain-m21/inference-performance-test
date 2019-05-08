#!/bin/bash

# Ex: ./scripts/vegeta_attack.sh tensorflow densenet121_tf 8501 ./data/densenet121_tf_payload.json 10 5 ./data/result_densenet121_tf_10_5

SERVING_TYPE=$1
MODEL_NAME=${2:-none}
PORT=$3
PAYLOAD=$4
RATE=$5
DURATION=$6
OUTPUT=${7:-data/vegeta_result.bin}

TF_ADDRESS="http://localhost:${PORT}/v1/models/${MODEL_NAME}:predict"
ONNX_ADDRESS="http://localhost:${PORT}/predict"

if [[ ${SERVING_TYPE} = "tensorflow" ]]; then
    ADDRESS=${TF_ADDRESS}
else
    ADDRESS=${ONNX_ADDRESS}
fi

echo -e "POST ${ADDRESS}\n\
Content-Type: application/json\n\
@${PAYLOAD}" > ./tools/target.txt

echo "Warm up serving before vegeta attack"
for i in `seq 10`
do
jq . ${PAYLOAD} | curl -s -o /dev/null -X POST ${ADDRESS} -H "Content-Type: application/json" -d @-
done

echo "Vegeta attack on ${SERVING_TYPE} ${MODEL_NAME} with rate = ${RATE}, duration = ${DURATION}, output = ${OUTPUT}"

VEGETA_OUTPUT=${OUTPUT}.bin
VEGETA_OUTPUT_JSON=${OUTPUT}.json

vegeta attack -rate=${RATE} -duration=${DURATION}s -targets=./tools/target.txt > ${VEGETA_OUTPUT}

cat ${VEGETA_OUTPUT} | vegeta report
cat ${VEGETA_OUTPUT} | vegeta report -type='hist[0,100ms,200ms,300ms,400ms,500ms,1s,2s,3s,4s,5s]'
cat ${VEGETA_OUTPUT} | vegeta report -type='json' | jq . > ${VEGETA_OUTPUT_JSON}
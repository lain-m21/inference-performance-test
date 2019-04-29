#!/bin/bash

RATE=$1
DURATION=$2
TARGET=${3:-tools/target.txt}
OUTPUT=${4:-tools/vegeta_result.bin}

echo "Vegeta attack - rate = ${RATE}, duration = ${DURATION}, target = ${TARGET}, output = ${OUTPUT}"

vegeta attack -rate=${RATE} -duration=${DURATION}s -targets=${TARGET} > ${OUTPUT}
cat vegeta.bin | vegeta report
cat vegeta.bin | vegeta report -type='hist[0,100ms,200ms,300ms,400ms,500ms,1s,2s,3s,4s,5s]'
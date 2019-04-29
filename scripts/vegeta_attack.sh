#!/bin/bash

RATE=$1
DURATION=$2
if [[ $# = 3 ]]; then
  OUTPUT=$3
else
  OUTPUT=tools/vegeta.bin
fi

vegeta attack -rate=${RATE} -duration=${DURATION}s -targets=tools/target.txt > ${OUTPUT}
cat vegeta.bin | vegeta report
cat vegeta.bin | vegeta report -type='hist[0,100ms,200ms,300ms,400ms,500ms,1s,2s,3s,4s,5s]'
#!/bin/bash

REST_PORT_TUNNEL=$1
SAVED_MODEL_NAME=$2

jq . ./tools/tf_payload.json | curl -X POST http://localhost:${REST_PORT_TUNNEL}/v1/models/${SAVED_MODEL_NAME}:predict -d @-
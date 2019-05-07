# inference-performance-test
Deep Learning models inference performance test

## Requirements
- Ubuntu 16.04, GCE VM instance is recommended
- install `go version go1.11.2 linux/amd64`
- Python version > 3.6.0
- Docker

## Flow
### 1. Install Vegeta attack
 
    make install-vegeta-attack


### 2. Build serving images 

    make build-all


### 3. Prepare a model 
    
    # TensorFlow Serving saved model
    python -m src.preparation.prepare_tf_model --model-name densenet121 --save-name densenet121_tf
    
    # ONNX Serving model
    python -m src.preparation.prepare_onnx_model --model-name densenet121 --save-name densenet121_onnx


### 4. Run serving image with prepared model

    # TensorFlow Serving
    ./scripts/run_tf_serving_optimized.sh densenet121_tf 8500 8501
    
    # ONNX Serving
    ./scripts/run_onnx_serving.sh sanic onnxruntime densenet121_onnx_info.json 18501

### 5. Prepare inputs for load test

    # TensorFlow Serving inputs
    python -m src.preparation.prepare_tf_inputs --model-info-path densenet121_tf_info.json --save-path densenet121_tf_payload.json
    
    # ONNX Serving inputs
    python -m src.preparation.prepare_onnx_inputs --model-info-path densenet121_onnx_info.json --save-path densenet121_onnx_payload.json


### 6. Run Vegeta attack to perform load test
    
    # TensorFlow Serving load test
    ./scripts/vegeta_attack.sh tensorflow densenet121_tf 8501 ./data/densenet121_tf_payload.json 10 5
    
    # ONNX Serving load test
    ./scripts/vegeta_attack.sh onnx densenet121 18501 ./data/densenet121_onnx_payload.json 10 5


## Findings
- `onnxruntime` conflicts with  `pytorch` when `conda` env is not used

## Todos
- `tensorflow-serving` gRPC client
- performance test on local
- performance test on k8s

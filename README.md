# inference-performance-test
Deep Learning models inference performance test

## Todos
- `tensorflow-model-server` docker build scripts
- `tensorflow-serving` gRPC client
- `torch` serving scripts
- performance test on local
- performance test on k8s

## Findings
- `onnxruntime` conflicts with  `pytorch` when `conda` env is not used
- `tensorflow_model_server` does inference much slower than `onnxruntime`
 even when optimized one is used,
 possibly because of the latency of `make_tensor_proto`
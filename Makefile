TF_SERVING_VERSION_GIT_BRANCH=r1.13
TF_SERVING_BUILD_OPTIONS=--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2 --copt=-O3
TF_SERVING_IMAGE=tensorflow/serving:latest
TF_SERVING_OPTIMIZED_IMAGE=tmp/tensorflow-serving-devel:0.0.1

ONNX_SERVING_IMAGE=tmp/onnx-serving:0.0.1

MODEL=densenet121
RATE=10
DURATION=5

.PHONY: pull-tf-serving-image
pull-tf-serving-image:
	docker pull ${TF_SERVING_IMAGE}

.PHONY: install-vegeta-attack
install-vegeta-attack:
	go get -u github.com/tsenart/vegeta

.PHONY: build-tf-serving-optimized-image
build-tf-serving-optimized-image:
	docker build --pull -t ${TF_SERVING_OPTIMIZED_IMAGE} \
    --build-arg TF_SERVING_VERSION_GIT_BRANCH="${TF_SERVING_VERSION_GIT_BRANCH}" \
    --build-arg TF_SERVING_BUILD_OPTIONS="${TF_SERVING_BUILD_OPTIONS}" \
    -f dockerfiles/Dockerfile.tf_serving.optimized .

.PHONY: build-onnx-image
build-onnx-image:
	docker build --pull -t ${ONNX_SERVING_IMAGE} \
	-f dockerfiles/Dockerfile.onnx_serving .

.PHONY: builld-all
build-all: build-tf-serving-optimized-image build-onnx-image

.PHONY: load-test-tf
load-test-tf:
	python -m src.preparation.prepare_tf_model --model-name ${MODEL} --save-name ${MODEL}_tf
	./scripts/run_tf_serving_optimized.sh ${MODEL}_tf 8500 8501
	python -m src.preparation.prepare_tf_inputs --model-info-path ${MODEL}_tf_info.json --save-path ${MODEL}_tf_payload.json
	./scripts/vegeta_attack.sh tensorflow ${MODEL}_tf 8501 ./data/${MODEL}_tf_payload.json 5 5 ./data/result_${MODEL}_tf_5_5.bin
	./scripts/vegeta_attack.sh tensorflow ${MODEL}_tf 8501 ./data/${MODEL}_tf_payload.json 10 5 ./data/result_${MODEL}_tf_10_5.bin
	./scripts/vegeta_attack.sh tensorflow ${MODEL}_tf 8501 ./data/${MODEL}_tf_payload.json 20 5 ./data/result_${MODEL}_tf_20_5.bin
	./scripts/vegeta_attack.sh tensorflow ${MODEL}_tf 8501 ./data/${MODEL}_tf_payload.json 30 5 ./data/result_${MODEL}_tf_30_5.bin


.PHONY: load-test-onnx
load-test-onnx:
	python -m src.preparation.prepare_onnx_model --model-name ${MODEL} --save-name ${MODEL}_onnx
	./scripts/run_onnx_serving.sh sanic onnxruntime ${MODEL}_onnx_info.json 18501
	./scripts/run_onnx_serving.sh sanic caffe2 ${MODEL}_onnx_info.json 28501
	python -m src.preparation.prepare_onnx_inputs --model-info-path ${MODEL}_onnx_info.json --save-path ${MODEL}_onnx_payload.json
	./scripts/vegeta_attack.sh onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 5 5 ./data/result_${MODEL}_onnxruntime_5_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 10 5 ./data/result_${MODEL}_onnxruntime_10_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 20 5 ./data/result_${MODEL}_onnxruntime_20_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 30 5 ./data/result_${MODEL}_onnxruntime_30_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 5 5 ./data/result_${MODEL}_caffe2_5_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 10 5 ./data/result_${MODEL}_caffe2_10_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 20 5 ./data/result_${MODEL}_caffe2_20_5.bin
	./scripts/vegeta_attack.sh onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 30 5 ./data/result_${MODEL}_caffe2_30_5.bin

.PHONY: clean-tf-serving
clean-tf-serving:
	docker container rm -f tf_serving

.PHONY: clean-onnx-serving
clean-onnx-serving:
	docker container rm -f onnxruntime_serving
	docker container rm -f caffe2_serving

.PHONY: clean-servings
clean-servings: clean-tf-serving clean-onnx-serving

.PHONY: clean-outputs-tf
clean-outputs-tf:
	rm -r data/${MODEL}_tf* data/result_${MODEL}_tf*

.PHONY: clean-outputs-onnx
clean-outputs-onnx:
	rm -r data/${MODEL}_onnx* data/result_${MODEL}_onnx*

.PHONY: clean-all-outputs
clean-all-outputs: clean-outputs-tf clean-outputs-onnx

.PHONY: load-test-and-clean
load-test-and-clean: load-test-tf load-test-onnx clean-servings clean-all-outputs

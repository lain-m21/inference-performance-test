TF_SERVING_VERSION_GIT_BRANCH=r1.13
TF_SERVING_BUILD_OPTIONS=--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2 --copt=-O3
TF_SERVING_IMAGE=tensorflow/serving:latest
TF_SERVING_OPTIMIZED_IMAGE=tmp/tensorflow-serving-devel:0.0.1
TF_SERVING_MKL_IMAGE=tmp/tensorflow-serving-mkl:0.0.1

ONNX_SERVING_IMAGE=tmp/onnx-serving:0.0.1

ONNXRUNTIME_SERVING_IMAGE=tmp/onnxruntime-serving:0.0.1

MODEL=densenet121
FRAMEWORK=sanic
RATE=10
DURATION=5

.PHONY: pull-tf-serving-base-image
pull-tf-serving-base-image:
	docker pull ${TF_SERVING_IMAGE}

.PHONY: install-vegeta-attack
install-vegeta-attack:
	go get -u github.com/tsenart/vegeta

.PHONY: build-tf-serving-optimized-base-image
build-tf-serving-optimized-base-image:
	docker build --pull -t ${TF_SERVING_OPTIMIZED_IMAGE} \
    --build-arg TF_SERVING_VERSION_GIT_BRANCH="${TF_SERVING_VERSION_GIT_BRANCH}" \
    --build-arg TF_SERVING_BUILD_OPTIONS="${TF_SERVING_BUILD_OPTIONS}" \
    -f dockerfiles/Dockerfile.tf_serving.optimized .

.PHONY: build-tf-serving-mkl-base-image
build-tf-serving-mkl-base-image:
	docker build --pull -t ${TF_SERVING_MKL_IMAGE} \
	-f dockerfiles/Dockerfile.tf_serving.mkl .

.PHONY: build-onnx-base-image
build-onnx-base-image:
	docker build --pull -t ${ONNX_SERVING_IMAGE} \
	-f dockerfiles/Dockerfile.onnx_serving .

.PHONY: build-onnxruntime-base-image
build-onnxruntime-base-image:
	docker build --pull -t ${ONNXRUNTIME_SERVING_IMAGE} \
	-f dockerfiles/Dockerfile.onnxruntime_serving .

.PHONY: load-test-tf
load-test-tf:
	python -m src.preparation.prepare_tf_model --model-name ${MODEL} --save-name ${MODEL}_tf

	./scripts/run_tf_serving_optimized.sh ${MODEL}_tf 8500 8501
	python -m src.preparation.prepare_tf_inputs --model-info-path ${MODEL}_tf_info.json --save-path ${MODEL}_tf_payload.json

	./scripts/load_test.sh tensorflow tensorflow ${MODEL}_tf ${MODEL} 8501 ./data/${MODEL}_tf_payload.json 5 5
	./scripts/load_test.sh tensorflow tensorflow ${MODEL}_tf ${MODEL} 8501 ./data/${MODEL}_tf_payload.json 10 5
	./scripts/load_test.sh tensorflow tensorflow ${MODEL}_tf ${MODEL} 8501 ./data/${MODEL}_tf_payload.json 20 5
	./scripts/load_test.sh tensorflow tensorflow ${MODEL}_tf ${MODEL} 8501 ./data/${MODEL}_tf_payload.json 30 5

.PHONY: load-test-onnx
load-test-onnx:
	python -m src.preparation.prepare_onnx_model --model-name ${MODEL} --save-name ${MODEL}_onnx

	./scripts/run_onnx_serving.sh ${FRAMEWORK} onnxruntime ${MODEL}_onnx_info.json 18501
	python -m src.preparation.prepare_onnx_inputs --model-info-path ${MODEL}_onnx_info.json --save-path ${MODEL}_onnx_payload.json

	./scripts/load_test.sh onnxruntime ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 5 5
	./scripts/load_test.sh onnxruntime ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 10 5
	./scripts/load_test.sh onnxruntime ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 20 5
	./scripts/load_test.sh onnxruntime ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 18501 ./data/${MODEL}_onnx_payload.json 30 5

	./scripts/run_onnx_serving.sh ${FRAMEWORK} caffe2 ${MODEL}_onnx_info.json 28501
	python -m src.preparation.prepare_onnx_inputs --model-info-path ${MODEL}_onnx_info.json --save-path ${MODEL}_onnx_payload.json

	./scripts/load_test.sh caffe2 ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 5 5
	./scripts/load_test.sh caffe2 ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 10 5
	./scripts/load_test.sh caffe2 ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 20 5
	./scripts/load_test.sh caffe2 ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 28501 ./data/${MODEL}_onnx_payload.json 30 5

.PHONY: load-test-onnxruntime
load-test-onnxruntime:
	python -m src.preparation.prepare_onnx_model --model-name ${MODEL} --save-name ${MODEL}_onnx

	./scripts/run_onnxruntime_serving.sh ${MODEL}_onnx 38501
	python -m src.preparation.prepare_onnxruntime_inputs --model-info-path ${MODEL}_onnx_info.json --save-path ${MODEL}_onnxruntime_payload.pb

	./scripts/load_test.sh onnxruntime_server ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 38501 ./data/${MODEL}_onnxruntime_payload.pb 5 5
	./scripts/load_test.sh onnxruntime_server ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 38501 ./data/${MODEL}_onnxruntime_payload.pb 10 5
	./scripts/load_test.sh onnxruntime_server ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 38501 ./data/${MODEL}_onnxruntime_payload.pb 20 5
	./scripts/load_test.sh onnxruntime_server ${FRAMEWORK} ${MODEL}_onnx ${MODEL} 38501 ./data/${MODEL}_onnxruntime_payload.pb 30 5

.PHONY: clean-tf-serving
clean-tf-serving:
	docker container rm -f tf_serving

.PHONY: clean-onnx-serving
clean-onnx-serving:
	docker container rm -f onnxruntime_serving
	docker container rm -f caffe2_serving

.PHONY: clean-onnxruntime-serving
clean-onnxruntime-serving:
	docker container rm -f onnxruntime_serving

.PHONY: clean-all-servings
clean-all-servings: clean-tf-serving clean-onnxruntime-serving

.PHONY: clean-tf-outputs
clean-tf-outputs:
	rm -r data/${MODEL}_tf*

.PHONY: clean-onnx-outputs
clean-onnx-outputs:
	rm -r data/${MODEL}_onnx*

.PHONY: clean-all-outputs
clean-all-outputs: clean-tf-outputs clean-onnx-outputs

.PHONY: load-test-and-clean
load-test-and-clean: load-test-tf load-test-onnxruntime clean-all-servings clean-all-outputs

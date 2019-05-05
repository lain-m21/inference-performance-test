TF_SERVING_VERSION_GIT_BRANCH="r1.13"
TF_SERVING_BUILD_OPTIONS="--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2 --copt=-O3"
TF_SERVING_IMAGE="tensorflow/serving:latest"
TF_SERVING_OPTIMIZED_IMAGE="tmp/tensorflow-serving-devel:0.0.1"

ONNX_SERVING_FLASK_IMAGE="tmp/onnx-serving-flask:0.0.1"
ONNX_SERVING_SANIC_IMAGE="tmp/onnx-serving-sanic:0.0.1"

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

.PHONY: build-onnx-flask-image
build-onnx-flask-image:
	docker build --pull -t ${ONNX_SERVING_FLASK_IMAGE} \
	--build-arg FRAMEWORK="flask" \
	-f dockerfiles/Dockerfile.onnx_serving .

.PHONY: build-onnx-sanic-image
build-onnx-sanic-image:
	docker build --pull -t ${ONNX_SERVING_SANIC_IMAGE} \
	--build-arg FRAMEWORK="sanic" \
	-f dockerfiles/Dockerfile.onnx_serving .

.PHONY: builld-all
build-all: build-tf-serving-optimized-image build-onnx-flask-image build-onnx-sanic-image

.PHONY: load-test-densenet121
load-test-densenet121:
	python -m src.preparation.prepare_tf_model --model-name densenet121 --save-name densenet121_tf
	python -m src.preparation.prepare_onnx_model --model-name densenet121 --save-name densenet121_onnx
	./scripts/run_tf_serving_optimized.sh densenet121_tf 8500 8501
	./scripts/run_onnx_serving.sh sanic onnxruntime densenet121_onnx_info.json 18501
	python -m src.preparation.prepare_tf_inputs --save-path densenet121_tf_payload.json
	python -m src.preparation.prepare_onnx_inputs --save-path densenet121_onnx_payload.json
	./scripts/vegeta_attack.sh tensorflow densenet121_tf 8501 ./data/densenet121_tf_payload.json 10 5
	./scripts/vegeta_attack.sh onnx densenet121 18501 ./data/densenet121_onnx_payload.json 10 5

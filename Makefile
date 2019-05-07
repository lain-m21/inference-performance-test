TF_SERVING_VERSION_GIT_BRANCH="r1.13"
TF_SERVING_BUILD_OPTIONS="--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2 --copt=-O3"
TF_SERVING_IMAGE="tensorflow/serving:latest"
TF_SERVING_OPTIMIZED_IMAGE="tmp/tensorflow-serving-devel:0.0.1"

ONNX_SERVING_IMAGE="tmp/onnx-serving:0.0.1"

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

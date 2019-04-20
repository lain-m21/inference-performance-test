TF_SERVING_VERSION_GIT_BRANCH="r1.13"
TF_SERVING_BUILD_OPTIONS="--copt=-mavx --copt=-mavx2 --copt=-mfma --copt=-msse4.1 --copt=-msse4.2"

.PHONY: build-tf-serving-optimized
build-tf-serving-optimized:
	docker build --pull -t tmp/tensorflow-serving-devel:0.0.1 \
    --build-arg TF_SERVING_VERSION_GIT_BRANCH="${TF_SERVING_VERSION_GIT_BRANCH}" \
    --build-arg TF_SERVING_BUILD_OPTIONS="${TF_SERVING_BUILD_OPTIONS}" \
    -f dockerfiles/Dockerfile.tf_serving.optimized .
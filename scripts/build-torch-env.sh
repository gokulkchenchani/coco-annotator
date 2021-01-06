#!/bin/bash

echo "[`basename "$0"`] Build docker python environment with PyTorch and CUDA support"

# check if a working path is provided
if [ -z "$1" ]
  then
    echo "[`basename "$0"`] No working path supplied, using pwd"
    BASE_PATH="."
  else
    BASE_PATH=$1
fi

echo "[`basename "$0"`] Building container..."
# Build docker python environment with torch and CUDA support
docker build --no-cache -f $BASE_PATH/../backend/Dockerfile.torch_env $BASE_PATH/../backend -t agrobot/coco-annotator:torch-python-env

echo "[`basename "$0"`] done building"

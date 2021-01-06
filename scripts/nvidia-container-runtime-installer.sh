#!/bin/bash

# @Author: Claus Smitt
# @Date:   2020-12-03 15:37:50
# @Last Modified by:   lvisroot
# @Last Modified time: 2020-12-04 15:16:29

echo "[`basename "$0"`] Install nvidia docker runtime support utils..."

# check if a working path is provided
if [ -z "$1" ]
  then
    echo "[`basename "$0"`] No working path supplied, using pwd"
    BASE_PATH="."
  else
    BASE_PATH=$1
fi

echo "[`basename "$0"`] Installing packages..."
# install docker container nvidia interface
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt install nvidia-container-runtime

# Enable nvidia support for docker containers by default
echo "[`basename "$0"`] Enable nvidia support for docker containers by default..."
sudo cp $BASE_PATH/cuda_support/daemon.json /etc/docker/daemon.json


echo "[`basename "$0"`] all done"

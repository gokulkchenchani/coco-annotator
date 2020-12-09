#!/bin/bash

# @Author: Claus Smitt
# @Date:   2020-12-03 15:37:50
# @Last Modified by:   lvisroot
# @Last Modified time: 2020-12-04 15:16:29

curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt install nvidia-container-runtime

sudo cp ./cuda_support/daemon.json /etc/docker/daemon.json

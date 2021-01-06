#!/bin/bash

# @Author: Claus Smitt
# @Date:   2020-12-07 17:01:59
# @Last Modified by:   Claus Smitt
# @Last Modified time: 2020-12-07 18:21:43

echo "[`basename "$0"`] Deploy keys generation..."

# check if a working path is provided
if [ -z "$1" ]
  then
    echo "[`basename "$0"`] No working path supplied, using pwd"
    BASE_PATH="."
  else
    BASE_PATH=$1
fi

# Create keys forder if it doesn't exist
if [ ! -d "$BASE_PATH/keys" ]
then
    echo "[`basename "$0"`] Creating deploy keys folder: $BASE_PATH/keys"
    mkdir $BASE_PATH/keys
fi
# generate deploy keys
echo "[`basename "$0"`] Creating deploy keys folder"
ssh-keygen -t rsa -b 4096 -f $BASE_PATH/keys/id_rsa_deploy_key -q -N ""

echo "[`basename "$0"`] Deploy keys saved successfully in: $BASE_PATH/keys"

#!/bin/bash

# @Author: Claus Smitt
# @Date:   2020-12-07 17:01:59
# @Last Modified by:   Claus Smitt
# @Last Modified time: 2020-12-07 18:21:43

# agrobot-pytorch-maskrcnn keygen
if [ ! -d "./keys" ]
then
    mkdir keys
fi
ssh-keygen -t rsa -b 4096 -f ./keys/id_rsa_agrobot_maskrcnn -q -N ""

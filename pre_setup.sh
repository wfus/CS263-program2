#!/usr/bin/env bash

# Do NOT change this file!


set -e

sudo apt-get update -qq
sudo apt-get install -qq -- \
    build-essential \
    curl \
    gcc \
    gcc-multilib \
    openssl \
    python \
    python3 \
    python-pip \
    python3-pip \
;

pip install -U --user \
    requests \
;
pip3 install -U --user \
    nose \
    requests \
;

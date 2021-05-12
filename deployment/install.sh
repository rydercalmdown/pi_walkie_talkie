#!/bin/bash
# install.sh

cd ../
sudo apt-get update
sudo apt-get install -y \
        python3-pip \
        libffi-dev \
        libssl-dev \
        mpg321 \
        portaudio19-dev
python3 -m pip install virtualenv
python3 -m virtualenv -p python3 env
. env/bin/activate

pip install -r src/requirements.txt

#!/bin/bash

sudo apt-get update
python -m pip install --user numpy \
                    matplotlib \
                    requests \
                    re \
                    seaborn \
                    pydub \
                    scipy

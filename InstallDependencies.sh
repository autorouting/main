#!/bin/bash

echo "Install conda on Python3"
python3 -m pip install conda

echo "Setup virtual environment"
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx
conda activate ox

# echo "Install ortools, geopy, networkx on Python3"
pip3 install ortools geopy networkx

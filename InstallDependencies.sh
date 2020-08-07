#!/bin/bash

echo "Setup virtual environment"
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx
conda activate ox

# echo "Install ortools, geopy, networkx"
pip3 install ortools geopy networkx

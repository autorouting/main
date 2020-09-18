#!/bin/bash

echo "Setup virtual environment"
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx
source activate ox

echo "Install ortools, geopy, networkx, googlemaps"
pip3 install ortools geopy networkx googlemaps

@ECHO OFF
TITLE Install Dependencies

ECHO Setup conda virtual environment
conda config --prepend channels conda-forge
conda create -n ox --strict-channel-priority osmnx
activate ox

ECHO Install ortools, geopy, networkx on Python3
pip install ortools geopy networkx

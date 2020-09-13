conda config --prepend channels conda-forge;
conda create -n ox --strict-channel-priority osmnx;
source activate ox;
python -m pip install --upgrade --user ortools;
python -m pip install geopy;
python -m pip install networkx;
python -m pip install googlemaps;
exit;
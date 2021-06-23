from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle
import numpy as np
import maputil


class BasicRouter():
    """
    The BasicRouter creates a routes using real world address.
    """

    def __init__(self, addresses: list, apikey: str, distancematrixoption=1):
        '''
        Args:
            addresses: list of all addresses (first address is origin, last address is destination)
            apikey: key for google map api, used to get coordinates of addresses
        '''
        self._addresses = addresses.copy()
        self._apikey = apikey

        #Construct self._coordinates
        self._coordinates = maputil.getcoordinate(self._addresses, apikey)

        #Construct distance matrix via Euclidean distance
        self._distancematrix = maputil.getdistancematrix(self._coordinates, option=distancematrixoption)

    def addIntermediateAddress():
        pass

    def routeOneVehicle(self):
        '''
        Returns: the optimized route assuming only the first driver is available
        '''
        pass

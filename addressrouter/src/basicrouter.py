from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import string
import random
import pickle
import numpy as np
import maputil


class BasicRouter():
    """
    The BasicRouter creates a routes using real world address.
    """

    def __init__(self, addresses: list, apikey: str, distancematrixoption=1, from_multi=False):
        '''
        Args:
            addresses: list of all addresses (first address is origin, last address is destination)
            apikey: key for google map api, used to get coordinates of addresses
        '''
        self.input_addresses = addresses
        self.api_key = apikey

        if not from_multi:
            #Construct self._coordinates
            self._coordinates = maputil.getcoordinates(self.input_addresses, apikey)

            #Construct distance matrix via Euclidean distance
            self.distance_matrix = self.distance_matrix(self._coordinates, option=distancematrixoption)

    def distance_matrix(self, coordpairs, distancematrixoption):
        self.distance_matrix = maputil.getdistancematrix(coordpairs, distancematrixoption)
        print(self.distance_matrix)
        return self.distance_matrix

    def addIntermediateAddress():
        pass

    def routeOneVehicle(self):
        '''
        Returns: the optimized route assuming only the first driver is available
        '''
        pass

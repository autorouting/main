from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle
import numpy as np


class BasicRouter():
    """
    The BasicRouter creates a routes using real world address.

    """

    def __init__(self, addresses, drivers, apikey):
        '''

        Args:
            addresses: list of all addresses
            drivers: list of 2-d arrays, containing the indices (in addresses) of the origin and destination of each driver
            apikey: key for google map api, used to get coordinates of addresses
        '''
        self._addresses = addresses
        self._drivers = drivers
        self._apikey = apikey

        #Construct self._coordinates
        pass
        self._coordinates = null

        #Construct distance matrix via Euclidean distance
        #self._distancematrix = null

    def update_distancematrix(self, newdistancematrix):
        '''

        Args:
            newdistancematrix:

        Returns:

        '''
        self._distancematrix = newdistancematrix

    def routeOneVehicle(self):
        '''

        Returns: the optimized route assuming only the first driver is available

        '''
        pass
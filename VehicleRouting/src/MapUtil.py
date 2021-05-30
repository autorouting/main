from __future__ import print_function
from geopy.geocoders import GoogleV3
import googlemaps as gmaps
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle


def getdistancematrix(coordinates, option=0):
    '''
    Args:
        coordinates: list of coordinates for N addresses
        option: 0 = Euclidean Distances; 1 = Driving Time from OpenStreetMap; 2 = ...

    Returns:
        the N by N distance matrix of based on the coordinates
    '''


def getpairdistance(coordinates):
    '''

    Args:
        coordinates: list of coordinates for 2 addresses

    Returns:

    '''

def getcoordinate(addresses, googleapikey):
    '''

    Args:
        addresses: a list of strings (each string is an address)
        googleapikey: string of google api key

    Returns:
        a list of coordinates (each coordinate contains a 2-d array)
    '''

    #Yikuan


if __name__ == '__main__':
    # test something here
    print("test")

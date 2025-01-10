from __future__ import print_function
import googlemaps as gmaps
import networkx as nx
# import osmnx as ox
import pickle
import concurrent.futures
import math
import requests
import urllib


# Initiate cache
geocode_cache = {}


def getdistancematrix(coordinates, option=0):
    '''
    Args:
        coordinates: list of coordinates for N addresses
        option: 0 = Euclidean Distances; 1 = Driving Time from OSRM API; 2 = ...
    Returns:
        the N by N distance matrix of based on the coordinates
    '''

    def fast_mode_distance_matrix(coordpairs):
        # initiate vars
        theMatrix = []
        # create 2d array with distances of node i -> node j
        for i in range(len(coordpairs)):
            theMatrix.append([])
            for j in range(len(coordpairs)):
                theMatrix[i].append(round(getpairdistance([coordpairs[i], coordpairs[j]], 0)))
        # output data
        return theMatrix
    
    def osrm_distance_matrix(coordpairs: list):
        rstring = "http://router.project-osrm.org/table/v1/driving/"
        coordsstring = []
        for coords in coordpairs:
            coordsstring.append(str(coords[1]) + "," + str(coords[0]))
            # lat/long seems to be reversed???
        rstring += ";".join(coordsstring)
        r = requests.get(rstring)
        theMatrix = r.json()["durations"]
        for r in range(len(theMatrix)):
            for c in range(len(theMatrix[r])):
                theMatrix[r][c] = round(theMatrix[r][c])
        return theMatrix

    if option == 0:
        return fast_mode_distance_matrix(coordinates)
    elif option == 1:
        return osrm_distance_matrix(coordinates)


def getpairdistance(coordinates, option=0):
    '''
    Args:
        coordinates: list of coordinates for 2 addresses
        option: 0 = Euclidean Distances; 1 = Driving Time from OSRM API; 2 = ...

    Returns:
        Calculated distance from coordinate 1 to coordinate 2
    '''

    def fast_mode_distance(coords1, coords2):
        DEGREE_TO_RAD = math.pi / 180
        DEGREE_LATITUDE = 111132.954  # 1 degree of longitude at the equator, in meters
        # convert coords to meters
        lon1 = coords1[1] * DEGREE_LATITUDE * math.cos(coords1[0] * DEGREE_TO_RAD)
        lon2 = coords2[1] * DEGREE_LATITUDE * math.cos(coords2[0] * DEGREE_TO_RAD)
        lat1 = coords1[0] * DEGREE_LATITUDE
        lat2 = coords2[0] * DEGREE_LATITUDE
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)
    
    if option == 0:
        return fast_mode_distance(coordinates[0], coordinates[1])
    elif option == 1:
        pass


def getcoordinate(addresses, googleapikey):
    '''
    Args:
        addresses: a list of strings (each string is an address)
        googleapikey: string of google api key
    Returns:
        a list of coordinates (each coordinate contains a 2-d array)
    '''

    # Yikuan
    def geocode_input(api_key, input, geolocator):
        # Use cache data if exists; otherwise, geocode
        if input in geocode_cache:
            location = geocode_cache[input]
        else:
            location = geolocator.geocode(input)
        coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])

        # Cache location object
        geocode_cache[input] = location

        return coords

    try:
        geolocator = gmaps.Client(key=googleapikey)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + googleapikey)
    # get inputs
    inputs = []
    for line in addresses:
        if (len(line.strip()) > 0):
            inputs.append(line.strip())

    # print(inputs)
    # print(inputs_first_thread)
    # print(inputs_subthread)
    # print(geocode_input(api_key, inputs_first_thread, geolocator))
    futures = []
    with concurrent.futures.ThreadPoolExecutor(4) as executer:
        for address in inputs:
            # print(address)
            future = executer.submit(geocode_input, googleapikey, address, geolocator)
            futures.append(future)
    # Wait until all are finished
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    results = [future.result() for future in futures]
    # print(results)
    coordpairs = []
    for i in range(len(results)):
        coordpairs.append(results[i])
    return coordpairs


def getmappedaddresses(addresses, googleapikey):
    '''

    Args:
        addresses: a list of strings (each string is an address)
        googleapikey: string of google api key

    Returns:
        a list of the formal addresses corresponding to addresses
    '''

    def geocode_input(api_key, input, geolocator):
        # Use cache data if exists; otherwise, geocode
        if input in geocode_cache:
            location = geocode_cache[input]
        else:
            location = geolocator.geocode(input)
        address = location[0]["formatted_address"]

        # Cache location object
        geocode_cache[input] = location

        return address

    try:
        geolocator = gmaps.Client(key=googleapikey)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + googleapikey)
    # get inputs
    inputs = []
    for line in addresses:
        if (len(line.strip()) > 0):
            inputs.append(line.strip())

    futures = []
    with concurrent.futures.ThreadPoolExecutor(4) as executer:
        for address in inputs:
            future = executer.submit(geocode_input, googleapikey, address, geolocator)
            futures.append(future)
    # Wait until all are finished
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    results = [future.result() for future in futures]
    mapped = []
    for i in range(len(results)):
        mapped.append(results[i])
    return mapped


def genmapslink(route: list):
    '''
    
    Args:
        route: a list of strings for every address in the route

    Returns:
        Google Maps directions link
    '''

    outstring = "https://www.google.com/maps/dir/"

    for address in route:
        outstring += urllib.parse.quote_plus(address) + "/"

    return outstring


if __name__ == '__main__':
    # test something here
    SYSTEM_TO_TEST = "geocode"

    if SYSTEM_TO_TEST == "geocode":
        myAddresses = """jade palace, chapel hill, NC
1101 mason farm	Chapel Hill
Timber Hollow court 	Chapel Hill
1105 W NC Highway 54 BYP, APT R9, Chapel hill	Chapel Hill""".splitlines()
        myKey = input("api key???\n > ")
        print(getcoordinate(myAddresses, myKey))
        print(getmappedaddresses(myAddresses, myKey))
    elif SYSTEM_TO_TEST == "distancematrix":
        print(getdistancematrix(
            [(35.910535, -79.07153699999999), (35.8993755, -79.0496993), (35.9407471, -79.055622), (35.8986969, -79.06878669999999), (35.918677, -79.0535469), (35.9528053, -79.0117215), (35.9305954, -79.0309678), (35.901634, -79.000045), (35.9538476, -79.06623789999999), (35.9187031, -79.0535469), (35.9333937, -79.03179519999999), (35.9317503, -79.029698), (35.9333937, -79.03179519999999), (35.9309288, -79.031252), (35.8980829, -79.0398685), (35.9317503, -79.029698), (35.9378711, -79.05453159999999), (35.8980563, -79.04115209999999), (35.89944070000001, -79.06600180000001)],
            option=0
        ))
    elif SYSTEM_TO_TEST == "mapslink":
        print(
            genmapslink(
                ['li ming’s global market', '390 Erwin Rd, Chapel Hill, NC', '100 Burnwood Ct, Chapel Hill, NC', '101 Palafox Dr, Chapel Hill, NC 27516', '311 Palafox Dr, Chapel Hill, NC 27516', '100 Manora Ln, Chapel Hill, NC 27516', '532 Lena Cir, Chapel Hill, NC', '1220 M.L.K. Jr Blvd, Chapel Hill, NC 27514', '118 Dixie Dr, Chapel Hill, NC 27514', '213 W Franklin St, Chapel Hill, NC 27516']
            )
        )
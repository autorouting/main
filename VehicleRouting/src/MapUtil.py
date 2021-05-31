from __future__ import print_function
import googlemaps as gmaps
import networkx as nx
#import osmnx as ox
import pickle
import concurrent.futures


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
    def geocode_input(api_key, input, geolocator):
        location = geolocator.geocode(input)
        coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
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

    #print(inputs)
    #print(inputs_first_thread)
    #print(inputs_subthread)
    #print(geocode_input(api_key, inputs_first_thread, geolocator))
    futures = []
    with concurrent.futures.ThreadPoolExecutor(4) as executer:
        for address in inputs:
            #print(address)
            future = executer.submit(geocode_input, googleapikey, address, geolocator)
            futures.append(future)
    # Wait until all are finished
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    results = [future.result() for future in futures]
    #print(results)
    coordpairs = []
    for i in range(len(results)):
        coordpairs.append(results[i])
    return coordpairs

if __name__ == '__main__':
    # test something here
    SYSTEM_TO_TEST = "geocode"
    
    if SYSTEM_TO_TEST == "geocode":
        print(getcoordinate("""jade palace, chapel hill, NC
1101 mason farm	Chapel Hill
Timber Hollow court 	Chapel Hill
1105 W NC Highway 54 BYP, APT R9, Chapel hill	Chapel Hill
602 Martin Luther King Jr BLVD	Chapel Hill
10104 Drew Hill Ln	Chapel Hill
214 Conner Dr Apt (Sunstone Apartment)	Chapel Hill
kingswood r9	Chapel Hill
117 Cabernet Dr, Chapel Hill	Chapel Hill
602 MLK Blv (lark chapel hill)	Chapel Hill
1521 E Franklin St, Chapel Hill	Chapel Hill
213 Conner Drive, Chapel Hill	Chapel Hill
1521 E Franklin St, Chapel Hill	Chapel Hill
203 Conner Dr Apt 5	Chapel Hill
1700 Baity Hill Dr Apt.110	Chapel Hill
213 Conner Drive, Apt 18	Chapel Hill
108 Shadowood Drive, Chapel Hill	Chapel Hill
1600 Baity Hill Dr	Chapel Hill
Laurel Ridge Apartment 25E	Chapel Hill""".splitlines(), input("api key???\n > ")))

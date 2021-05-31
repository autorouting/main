from __future__ import print_function
import googlemaps as gmaps
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import concurrent.futures
import time
import database
import client1
import serialize
import math
import multiprocessing
import requests

def parallel_geocode_inputs(api_key, fakeinputfile, max_workers = 2):
    """
    Use parallel processing to process inputted addresses as geocode
    
    Parameters:
    api_key (string): Google API key
    fakeinputfile (string): user inputted addresses
    
    Returns:
    string: The google maps link of the route.
    """
    try:
        geolocator = gmaps.Client(key=api_key)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + api_key)
    # get inputs
    inputs = []
    for line in fakeinputfile.split("\n"):
        if (len(line.strip()) > 0):
            inputs.append(line.strip())

    #print(inputs)
    #print(inputs_first_thread)
    #print(inputs_subthread)
    #print(geocode_input(api_key, inputs_first_thread, geolocator))
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executer:
        for address in inputs:
            #print(address)
            future = executer.submit(geocode_input, api_key, address, geolocator)
            futures.append(future)
    # Wait until all are finished
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    results = [future.result() for future in futures]
    #print(results)
    faulty_addresses = []
    addresses = []
    coordpairs = []
    for i in range(len(results)):
        if results[i][1] != None: 
            addresses.append(results[i][1])
            coordpairs.append(results[i][2])
        else:
            faulty_addresses.append(results[i][0]) 
            addresses.append(None)
            coordpairs.append(None)
    return (faulty_addresses, addresses, coordpairs, inputs)

def geocode_input(api_key, input, geolocator):
    """
    Use parallel processing to process inputted addresses as geocode
    
    Parameters:
    api_key (string): Google API key
    input (string): user inputted addresses
    geolocator: object from Google Maps API that generate geocode of address
    
    Returns:
    string[]: List of incorrect addresses
    string[]: formatted addresses of the inputted addresses
    float[]: coordinates of each address
    string: original inputted addresses
    """
    #lessThanOneInt = True
    #time.sleep(1)
    #print(input)
    faultyAddress = None
    coords = None
    address = None
    #print('1')
    # for every line of input, generate location object
    placeid = database.fetch_placeid(input)
    if len(placeid) == 0:
        try:
            location = geolocator.geocode(input + " NC") # IMPORTANT: NC must be changed for usage in different states.
            coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
            address = location[0]["formatted_address"]
            database.insert_data(input, location[0]['place_id'], coords[0], coords[1], address)
        except:
            faultyAddress = str(input)
            #print(faultyAddress)
    else:
        out_data = database.fetch_output_data(placeid[0][0])
        address = out_data[0][2]
        coords = [float(out_data[0][0]), float(out_data[0][1])]
    # output data
    return (faultyAddress, address, coords, input)

def fast_mode_distance(coords1, coords2):
    """
    Calculate distance between two coordinates

    Parameters:
    coords1 (list): The coordinates for address one.
    coords2 (list): The coordinates for address two.

    Returns:
    float: The distance between the coordinates
    """
    DEGREE_TO_RAD = math.pi / 180
    DEGREE_LATITUDE = 111132.954 # 1 degree of longitude at the equator, in meters
    # convert coords to meters
    lon1 = coords1[1] * DEGREE_LATITUDE * math.cos(coords1[0] * DEGREE_TO_RAD)
    lon2 = coords2[1] * DEGREE_LATITUDE * math.cos(coords2[0] * DEGREE_TO_RAD)
    lat1 = coords1[0] * DEGREE_LATITUDE
    lat2 = coords2[0] * DEGREE_LATITUDE
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def fast_mode_distance_matrix(coordpairs):
    """
    Create fast mode distance matrix

    Parameters:
    coordpairs (array): Coordinate for each

    Returns:
    array: The distance matrix calculated by direct distance between coordinates
    """
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first
    # initiate vars
    theMatrix = []
    # create 2d array with distances of node i -> node j
    for i in range(len(coordpairs)):
        theMatrix.append([])
        for j in range(len(coordpairs)):
            theMatrix[i].append(fast_mode_distance(coordpairs[i], coordpairs[j]))
    # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
    for i in range(2, len(theMatrix)):
        theMatrix[i][1] = MAX_DISTANCE
    # output data
    return theMatrix

def osrm_distance_matrix(coordpairs: list):
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first
    rstring = "http://router.project-osrm.org/table/v1/driving/"
    coordsstring = []
    for coords in coordpairs:
        coordsstring.append(str(coords[0]) + "," + str(coords[1]))
    rstring += ";".join(coordsstring)
    r = requests.get(rstring)
    theMatrix = r.json()["durations"]
    # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
    for i in range(2, len(theMatrix)):
        theMatrix[i][1] = MAX_DISTANCE
    return theMatrix
    
def create_data_model(distancematrix):
    """
    Create a dictionary/data model
    
    Parameters:
    distancematrix (float[][]): array of distances between addresses
    
    Returns:
    dictionary: data model generated
    """
    # initiate ORTools
    data = {}
    data['distance_matrix'] = distancematrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return (data)

def print_solution(manager, routing, solution, addresses):
    """
    Creates a displayable version of the solution
    
    Parameters:
    routing (): 
    routing ():
    solution ():
    addresses ():
    
    Returns:
    string[]: solution generated by application
    """
    # create ORTools solution
    #print('Objective: {} meters'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = []
    route_distance = 0
    while not routing.IsEnd(index):
        if index:
            plan_output.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if index:
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output.append(manager.IndexToNode(index))
    return plan_output

def main(api_key, fakeinputfile, fast_mode_toggled):
    #process addresses and check for faulty ones
    #start_time = time.perf_counter_ns()
    faultyAddress, addresses, coordpairs, inputs = parallel_geocode_inputs(api_key, fakeinputfile, 4)
    if len(faultyAddress) == 0:
        # run ORTools
        if fast_mode_toggled:
            distancematrix = fast_mode_distance_matrix(coordpairs)
        else:
            distancematrix = osrm_distance_matrix(coordpairs)
        data = create_data_model(distancematrix)
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        solution = routing.SolveWithParameters(search_parameters)
        ordered_indeces = print_solution(manager, routing, solution, addresses)
        if solution:
            ordered_indeces
        route_solution = []
        route_solution_nonformatted = []
        ordered_coords = []
        for x in ordered_indeces:
            route_solution.append(addresses[x])
            route_solution_nonformatted.append(inputs[x])
            ordered_coords.append(str(coordpairs[x][0]) + "," + str(coordpairs[x][1]))
        #end_time = time.perf_counter_ns()
        #print((end_time - start_time) / 10 ** 9)
        return (route_solution, ordered_coords, route_solution_nonformatted, ordered_indeces)
    else:
        output = "<h1>Incorrect addresses</h1>"
        for address in faultyAddress:
            #print(address)
            output += "<p style=\"color:Tomato;\">" + address + "</p>"
            #print('\n' + output)
        #print(1)
        return(output, "", "yee")

if __name__ == '__main__':
    # run the main script
    # locations.txt: line 1: destination?
    # locations.txt: line 2: origin?
    # locations.txt: line 3-: intermediate addresses
    print(main(input("API key:\n "), open("locations.txt", "r").read(), False)[0].replace("<br>", "\n").replace("<B>", "\n\t").replace("</B>", "\t").replace("<h1>", "\n\t").replace("</h1>", "\t\n").replace("<p style=\"color:Tomato;\">", " ").replace("</p>", "\t\n"))
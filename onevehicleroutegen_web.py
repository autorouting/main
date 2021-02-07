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
import math
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import time

def parallel_geocode_inputs(api_key, fakeinputfile, max_workers = 2):
    try:
        geolocator = gmaps.Client(key=api_key)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + api_key)

    # get inputs
    inputs = fakeinputfile.split("\n")
    print(inputs)
    """
    inputs_first_thread = []
    inputs_second_thread = []
    for i in range(len(inputs)):
        if inputs[i] != "" and inputs[i] != " ":
            if i%2 == 0:
                inputs_first_thread.append(inputs[i])

    """
    #print(inputs)
    #print(inputs_first_thread)
    #print(inputs_subthread)

    #print(geocode_input(api_key, inputs_first_thread, geolocator))

    futures = []
    
    try:
        # read database
        prevGeocodes = pickle.load( open( "prev_geocodes.p", "rb" ) )
    except:
        # create database
        pickle.dump( {}, open( "prev_geocodes.p", "wb" ) )
        # read database
        prevGeocodes = pickle.load( open( "prev_geocodes.p", "rb" ) )
    
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executer:
        for address in inputs:
            #print(address)
            future = executer.submit(geocode_input, api_key, address, geolocator, prevGeocodes)
            futures.append(future)
    
    # Wait until all are finished
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    
    results = [future.result() for future in futures]
    #print(results)

    faulty_addresses = []
    addresses = []
    coords = []
    for i in range(len(results)):
        if results[i][1] != None: 
            addresses.append(results[i][1])
            coords.append(results[i][2])
        else:
            faulty_addresses.append(results[i][0]) 
            addresses.append(None)
            coords.append(None)

    return (faulty_addresses, addresses, coords)



def geocode_input(api_key, input, geolocator, prevGeocodes):
    #lessThanOneInt = True
    #time.sleep(1)
    print(input)
    faultyAddress = None
    coords = None
    address = None
    #print('1')
    # for every line of input, generate location object
    try:
        # if datapoint is already in database, use the previously called output; otherwise, create a new request
        # this will help save money on Google API, as repeated requests are unnecessary
        if input in prevGeocodes:
            location = prevGeocodes[input]
        else:
            location = geolocator.geocode(input)
            prevGeocodes[input] = location # add new datapoint to database

        coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
        address = location[0]["formatted_address"]
    except:
        faultyAddress = "<B>Address(es): </B>" + str(input)
        print(faultyAddress)
    
    pickle.dump( prevGeocodes, open( "prev_geocodes.p", "wb" ) )

    # output data
    #print(coords)
    return (faultyAddress, address, coords)

def fast_mode_distance(coords1, coords2):
    DEGREE_TO_RAD = math.pi / 180
    DEGREE_LATITUDE = 111132.954 # 1 degree of longitude at the equator, in meters
    # convert coords to meters
    lon1 = coords1[1] * DEGREE_LATITUDE * math.cos(coords1[0] * DEGREE_TO_RAD)
    lon2 = coords2[1] * DEGREE_LATITUDE * math.cos(coords2[0] * DEGREE_TO_RAD)
    lat1 = coords1[0] * DEGREE_LATITUDE
    lat2 = coords2[0] * DEGREE_LATITUDE
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


def generate_distance_matrix(nodes, G):
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first

    # initiate vars
    if not fast_mode_toggled:
        # load previously saved graph; unneeded if not fast mode
        G = pickle.load(open("graph", "rb"))
    else:
        G = "who cares really about this(if fast mode is off)? this is just to prevent error"

    output_list = []

    # create 2d array with distances of node i -> node j
        
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    
    # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
    for i in range(2, len(output_list)):
        output_list[i][1] = MAX_DISTANCE
    
    # output data
    return (output_list)

def create_data_model(distancematrix):
    # initiate ORTools
    data = {}
    data['distance_matrix'] = distancematrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return (data)

def print_solution(manager, routing, solution, addresses):
    # create ORTools solution
    #print('Objective: {} meters'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = '<B>Route for vehicle 0:</B><br>'
    route_distance = 0
    textfileoutput = ""
    while not routing.IsEnd(index):
        if index:
            plan_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
            textfileoutput += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        if index:
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    textfileoutput += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    #outputfile = open("route.txt", "w")
    #outputfile.write(textfileoutput)
    #outputfile.close()
    #plan_output += '<P><B>Route distance: {} meters</B></P>'.format(route_distance)
    #print(plan_output)
    return plan_output, textfileoutput

def main(api_key, fakeinputfile):
    #process addresses and check for faulty ones

    start_time = time.perf_counter_ns()
    faultyAddress, addresses, coords = parallel_geocode_inputs(api_key, fakeinputfile)

    if len(faultyAddress) == 0:
        # run ORTools
        distancematrix = generate_distance_matrix(nodes, G)
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
        route_solution, stringoutput = print_solution(manager, routing, solution, addresses)
        if solution:
            route_solution
        end_time = time.perf_counter_ns()
        print((end_time - start_time) / 10 ** 9)
        return (route_solution.replace("->", " -><br>"), stringoutput)
    else:
        output = "<h1>Incorrect address(es)</h1>"

        for address in faultyAddress:
            print(address)
            output += "<p style=\"color:Tomato;\">" + address + "</p>"
            print('\n' + output)

        print(1)
        return(output, "")

if __name__ == '__main__':
    # run the main script
    # locations.txt: line 1: destination?
    # locations.txt: line 2: origin?
    # locations.txt: line 3-: intermediate addresses
    print(main(input("API key:\n "), open("locations.txt", "r").read(), True)[0].replace("<br>", "\n").replace("<B>", "\n\t").replace("</B>", "\t").replace("<h1>", "\n\t").replace("</h1>", "\t\n").replace("<p style=\"color:Tomato;\">", " ").replace("</p>", "\t\n"))

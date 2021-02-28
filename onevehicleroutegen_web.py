from __future__ import print_function
from geopy.geocoders import GoogleV3
import googlemaps as gmaps
import networkx as nx
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle
import math
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
#import time
import database
import distancematrix_web

def parallel_geocode_inputs(api_key, fakeinputfile, G, max_workers = 2):
    try:
        geolocator = gmaps.Client(key=api_key)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + api_key)
    # get inputs
    inputs = fakeinputfile.split("\n")
    for i in range(len(inputs)):
        inputs[i] = inputs[i].strip() # remove unnecessary spaces or return characters (\r) from input
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
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executer:
        for address in inputs:
            #print(address)
            future = executer.submit(geocode_input, api_key, address, geolocator, G)
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
    return (faulty_addresses, addresses, coordpairs)

def geocode_input(api_key, input, geolocator, G):
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
            location = geolocator.geocode(input)
            coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
            address = location[0]["formatted_address"]
            database.insert_data(input, location[0]['place_id'], coords[0], coords[1], address, str(6969))
        except:
            faultyAddress = "<B>Address(es): </B>" + str(input)
            #print(faultyAddress)
    else:
        out_data = database.fetch_output_data(placeid[0][0])
        address = out_data[0][2]
        coords = [float(out_data[0][0]), float(out_data[0][1])]
    # output data
    return (faultyAddress, address, coords)

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
    #start_time = time.perf_counter_ns()
    G = pickle.load( open("graph", "rb") )
    faultyAddress, addresses, coordpairs = parallel_geocode_inputs(api_key, fakeinputfile, G, 4)
    if len(faultyAddress) == 0:
        # run ORTools
        distancematrix = distancematrix_web.generate_distance_matrix(coordpairs, G)
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
        #end_time = time.perf_counter_ns()
        #print((end_time - start_time) / 10 ** 9)
        return (route_solution.replace("->", " -><br>"), stringoutput)
    else:
        output = "<h1>Incorrect address(es)</h1>"
        for address in faultyAddress:
            #print(address)
            output += "<p style=\"color:Tomato;\">" + address + "</p>"
            #print('\n' + output)
        #print(1)
        return(output, "")

if __name__ == '__main__':
    # run the main script
    # locations.txt: line 1: destination?
    # locations.txt: line 2: origin?
    # locations.txt: line 3-: intermediate addresses
    print(main(input("API key:\n "), open("locations.txt", "r").read())[0].replace("<br>", "\n").replace("<B>", "\n\t").replace("</B>", "\t").replace("<h1>", "\n\t").replace("</h1>", "\t\n").replace("<p style=\"color:Tomato;\">", " ").replace("</p>", "\t\n"))
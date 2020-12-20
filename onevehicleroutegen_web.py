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

def take_inputs(api_key, fakeinputfile):

    geolocator = gmaps.Client(key=api_key)

    # get inputs
    inputs = fakeinputfile.split("\n")

    # initiate vars
    addresses = []
    locations = []
    coords = []
    faultyAddress = []
    lessThanOneInt = True
    
    # for every line of input, generate location object
    for i in range(0, len(inputs)):
        try:
            location = geolocator.geocode(inputs[i])
            print("inputs[i]:", inputs[i])
            if len(location) == 0:
                raise "errorerrorerror"
            addresses.append(inputs[i])
            locations.append(location)
        except:
            if i == 0:
                faultyAddress.append("Destination Address(s): ")
            elif i == 1:
                faultyAddress.append("Origin Address(s): ")
            elif lessThanOneInt:
               faultyAddress.append("Intermediate Address(s): ")
               lessThanOneInt = False
            faultyAddress.append(inputs[i])

    # generate coords & nodes
    if len(faultyAddress) == 0:
        i = 0
        for i in range(len(locations)):
            coords.append((locations[i][0]['geometry']['location']['lat'], locations[i][0]['geometry']['location']['lng']))


    # output data
    #print(coords)
    return (faultyAddress, addresses, coords)

def fast_mode_distance(coords1, coords2):
    # convert coords to meters
    lon1 = coords1[1] * 111132.954 * math.cos(coords1[0] * math.pi / 180)
    lon2 = coords2[1] * 111132.954 * math.cos(coords2[0] * math.pi / 180)
    lat1 = coords1[0] * (111132.954  - 559.822 * math.cos(2 * coords1[0] * math.pi / 180) + 1.175 * math.cos(4 * coords1[0] * math.pi / 180))
    lat2 = coords2[0] * (111132.954  - 559.822 * math.cos(2 * coords2[0] * math.pi / 180) + 1.175 * math.cos(4 * coords2[0] * math.pi / 180))
    return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

def generate_distance_matrix(coords, fast_mode_toggled):
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first

    # initiate vars
    if not fast_mode_toggled:
        # load previously saved graph; unneeded if not fast mode
        G = pickle.load(open("graph", "rb"))
    else:
        G = "who cares really (if fast mode is off)? this is just to prevent error"

    # create 2d array with distances of node i -> node j
    if fast_mode_toggled:
        output_list = []
        for i in range(len(coords)):
            output_list.append([])
            for j in range(len(coords)):
                output_list[i].append(fast_mode_distance(coords[i], coords[j]))
        # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
        for i in range(2, len(output_list)):
            output_list[i][1] = MAX_DISTANCE
    else:
        # Generate nodes
        nodes = []
        for i in range(len(coords)):
            nodes.append(ox.get_nearest_node(G, coords[i]))

        output_list = []
        
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

def main(api_key, fakeinputfile, fast_mode_toggled):
    #process addresses and check for faulty ones
    faultyAddress, addresses, coords = take_inputs(api_key, fakeinputfile)
    if len(faultyAddress) == 0:
        # run ORTools
        distancematrix = generate_distance_matrix(coords, fast_mode_toggled)
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
        #print(route_solution)
        return (route_solution.replace("->", " -><br>"), stringoutput)
    else:
        output = "<h1>Incorrect address(es)</h1>"
        for address in faultyAddress:
            output += "<p style=\"color:Tomato;\">" + address + "</p>"
        return(output, "")

if __name__ == '__main__':
    # run the main script
    # locations.txt: line 1: destination?
    # locations.txt: line 2: origin?
    # locations.txt: line 3-: intermediate addresses
    main(input("API key:\n "), open("locations.txt", "r").read(), True)
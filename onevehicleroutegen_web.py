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

def take_inputs(api_key, fakeinputfile):

    geolocator = gmaps.Client(key=api_key)

    # load previously saved graph
    G = pickle.load(open("graph", "rb"))

    # get inputs
    inputs = fakeinputfile.split("\n")

    # initiate vars
    addresses = []
    locations = []
    coords = []
    nodes = []

    # for every line of input, generate location object
    i = 0
    while True:

        addresses.append(inputs[i])
        try:
            locations.append(geolocator.geocode(addresses[i]))
            if len(locations[i]) == 0:
                locations.pop(i)
                raise "errorerrorerror"
            i += 1
        except:
            addresses.pop(i)
            inputs.pop(i)
        
        if i == len(inputs):
            break

    #print(addresses)
    #print(locations[len(locations) - 1])

    # generate coords & nodes
    i = 0
    for i in range(len(locations)):
        coords.append((locations[i][0]['geometry']['location']['lat'], locations[i][0]['geometry']['location']['lng']))
        nodes.append(ox.get_nearest_node(G, coords[i]))


    # output data
    return (G, nodes, addresses)

def generate_distance_matrix(api_key, fakeinputfile):
    # initiate vars
    G, nodes, addresses = take_inputs(api_key, fakeinputfile)

    # create 2d array with distances of node i -> node j
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    
    # rig distance so that optimization algorithm chooses to go to restaraunt asap (after depot)
    for i in range(2, len(output_list)):
        output_list[i][1] = 7666432.01
    
    # output data
    return (output_list, addresses)

def create_data_model(api_key, fakeinputfile):
    # create distance matrix; also get corresponding addresses
    distancematrix, addresses = generate_distance_matrix(api_key, fakeinputfile)
    # initiate ORTools
    data = {}
    data['distance_matrix'] = distancematrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return (addresses, data)

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
    plan_output += '<P><B>Route distance: {} meters</B></P>'.format(route_distance)
    #print(plan_output)
    return plan_output, textfileoutput

def main(api_key, fakeinputfile):
    # run ORTools
    addresses, data = create_data_model(api_key, fakeinputfile)
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

    return (route_solution.replace("->", " -><br>"), stringoutput)

if __name__ == '__main__':
    # run the main script
    # locations.txt: line 1: destination?
    # locations.txt: line 2: origin?
    # locations.txt: line 3-: intermediate addresses
    main(input("API key:\n "), open("locations.txt", "r").read())
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
from itertools import combinations

def take_inputs(api_key):
    global G
    global addresses
    global nodes

    geolocator = gmaps.Client(key=api_key)

    # load previously saved graph
    G = pickle.load(open("graph", "rb"))

    # open input file
    inputfile = open("locations.txt", "r")
    inputs = inputfile.read().split("\n")
    inputfile.close() # close it

    # initiate vars
    addresses = []
    locations = []
    coords = []
    nodes = []

    # for every line of input, generate location object
    for i in range(len(inputs)):

        addresses.append(inputs[i])
        try:
            locations.append(geolocator.geocode(addresses[i]))
        except:
            error_found = "faulty input at line {} of locations.txt".format(i + 1)
        #if locations[i] == None:
            #print("faulty input at line {} of locations.txt".format(i + 1))

    # generate coords & nodes
    i = 0
    for i in range(len(locations)):
        coords.append((locations[i][0]['geometry']['location']['lat'], locations[i][0]['geometry']['location']['lng']))
        nodes.append(ox.get_nearest_node(G, coords[i]))


    # output data
    return (G, nodes, addresses)

def generate_distance_matrix(api_key):
    # initiate vars
    G, nodes, addresses = take_inputs(api_key)

    # create 2d array with distances of node i -> node j
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    
    # output data
    return (output_list, addresses)

def create_data_model(api_key):
    # create distance matrix; also get corresponding addresses
    distancematrix, addresses = generate_distance_matrix(api_key)
    # initiate ORTools
    data = {}
    data['distance_matrix'] = distancematrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return (addresses, data)

def print_solution(manager, routing, solution, addresses):
    # create ORTools solution
    print('Objective: {} meters'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 1:\n'
    route_distance = 0
    textfileoutput = ""
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        textfileoutput += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    textfileoutput += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    outputfile = open("route.txt", "w")
    outputfile.write(textfileoutput)
    outputfile.close()
    plan_output += 'Route distance: {}km\n'.format(str(int(route_distance) / 1000))
    return plan_output

def main(api_key):
    # run ORTools
    addresses, data = create_data_model(api_key)
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
    route_solution = print_solution(manager, routing, solution, addresses)
    if solution:
        split_route()
def split_route():
    route = open("route.txt", "r")
    route = route.read()
    route = str(route).split(" -> ")
    i = 1
    while i > len(route):
        if route[i] == '\n':
            route.remove(route)
            i -= 1
        i += 1 

    for j in range(len(route)):
        if '\n' in list(route[j]):
            temp = list(route[j])
            temp.remove('\n')
            route[j] = ''.join(temp)
        
        if ' ' == list(route[j])[0]:
            temp = list(route[j])
            temp.pop(0)
            route[j] = ''.join(temp)
    
    start = route[0]

    chunks = []
    for combs in [combinations(route, num) for num in range(len(route) + 1)]:
        for comb in combs:
            comb = list(set(comb))
            chunk = [list(comb)]
            diff = list(set(route) - set(comb))
            if start in diff:
                comb.insert(0, start)

            else:
                diff.insert(0, start)

            chunk.append(diff)
            chunks.append(chunk)
    
    total_distance = []

    for i in range(len(chunks)):
        for j in range(2):
            temp = [0, 0]
            for l in range(1, len(chunks[i][j])):
                temp[j] += nx.shortest_path_length(G, nodes[addresses.index(chunks[i][j][l - 1])], nodes[addresses.index(chunks[i][j][l])], weight='length')
            temp[j] *= -1
        total_distance.append(temp)
    print(chunks)   
    print(total_distance)
    optimizer = max_value(total_distance)
    print(chunks[optimizer[0]])
    

    
def max_value(test):
    max_sublist = []
  
    for i in range(len(test)):
        max_sublist.append([test[i].index(max(test[i])), max(test[i])])
        largest = [0, -1]
        
        for i in range(len(max_sublist)):
            if max_sublist[i][-1] > max_sublist[largest[0]][largest[1]]:
                largest = [i, -1]

    largest_sublist = test[largest[0]]
    largest = [largest[0], largest_sublist.index(max(largest_sublist))]
    return largest



if __name__ == '__main__':
    # run the main script
    main(input("API key:\n "))
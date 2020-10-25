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
from time import perf_counter

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
        split_route(data['distance_matrix'])

def split_route(distance_matrix):
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
    
    start_end = route[0]
    chunks = sorted_k_partitions(route, int(input('How many drivers are there?  ')), start_end)
    total_distance = [[] for sub_route in chunks]
    
    for i in range(len(chunks)):
        for j in range(len(chunks[i])):
            temp = 0
            for l in range(1, len(chunks[i][j])):
                temp += distance_matrix[addresses.index(chunks[i][j][l - 1])][addresses.index(chunks[i][j][l])]
            temp *= -1
            total_distance[i].append(temp)

    optimizer_shortest = max_value(total_distance)
    optimizer_min_average = min_average(total_distance)
    optimizer_min_deviance = min_deviance(total_distance)

    print(chunks[optimizer_shortest[0]])
    print(chunks[optimizer_min_average])
    print(chunks[optimizer_min_deviance])
    
def sorted_k_partitions(tsp_route, k, start_end):
    n = len(tsp_route)
    groups = []

    def generate_partitions(i):
        if i >= n:
            yield list(map(list, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(tsp_route[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([tsp_route[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    routes = generate_partitions(0)

    routes = [sorted(ps, key = lambda p: (len(p), p)) for ps in routes]
    routes = sorted(routes, key = lambda ps: (*map(len, ps), ps))
    
    for i in range(len(routes)):
      for j in range(len(routes[i])):
        if routes[i][j][0] != start_end:
          routes[i][j].insert(0, start_end)
        if routes[i][j][-1] != start_end:
          routes[i][j].append(start_end)


    return routes

def max_value(distances):
    max_sublist = []
  
    for i in range(len(distances)):
        max_sublist.append([distances[i].index(max(distances[i])), max(distances[i])])
        largest = [0, -1]
        
        for i in range(len(max_sublist)):
            if max_sublist[i][-1] > max_sublist[largest[0]][largest[1]]:
                largest = [i, -1]

    largest_sublist = distances[largest[0]]
    largest = [largest[0], largest_sublist.index(max(largest_sublist))]
    return largest

def min_average(distances):
    avgs = []

    for i in range(len(distances)):
        avg = sum(distances[i]) / len(distances[i])
        avgs.append(avg)

    return avgs.index(max(avgs))

def min_deviance(distances):
    avgs = []
    
    for i in range(len(distances)):
        avg = sum(distances[i]) / len(distances[i])
        avgs.append(avg)   

    mads = []

    for i in range(len(distances)):
        temp = 0
        for j in range(len(distances[i])):
            difference = ((avgs[i] - distances[i][j]) ** 2) ** 0.5
            temp += difference
        
        mads.append(temp)

    return mads.index(min(mads))   




if __name__ == '__main__':
    # run the main script
    main(input("API key:\n "))
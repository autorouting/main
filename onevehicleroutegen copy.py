from __future__ import print_function
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle

#choose random string to use for Nominatim app name
def gen_rand_key():
    symbols = list(string.ascii_lowercase)

    for i in range(10):
        symbols.append(str(i))
    
    key = []
    
    for i in range(10):
        key.append(random.choice(symbols))
    
    return ''.join(key)

def take_inputs():

    while True:
        try:
            geolocator = Nominatim(user_agent = gen_rand_key())
            break # if all goes smoothly, go on
        except:
            joe = "joe" # just to fill in the except; doesn't have real meaning
            # retry key generation

    # load previously saved graph
    G = pickle.load(open("graph", "rb"))
    #G = ox.graph_from_place(input("place of which to generate graph (ex.: Orange County, NC, USA):\n "), network_type='drive')
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
        locations.append(geolocator.geocode(addresses[i]))
        #if locations[i] == None:
            #print("faulty input at line {} of locations.txt".format(i + 1))
    
    # remove faulty locations
    i = 0
    while i < len(locations):
        if locations[i] == None:
            locations.remove(locations[i])
            i -= 1
        
        i += 1

    # generate coords & nodes
    i = 0
    for i in range(len(locations)):
        coords.append((locations[i].latitude, locations[i].longitude))
        print(coords[i])
        print(ox.get_nearest_node(G, coords[i]))
        nodes.append(ox.get_nearest_node(G, coords[i]))


    # output data
    print(nodes)
    print(addresses)
    print("Locations: " + str(locations))
    return (G, nodes, addresses)

def generate_distance_matrix():
    # initiate vars
    G, nodes, addresses = take_inputs()

    # create 2d array with distances of node i -> node j
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    
    
    # rig distance so that optimization algorithm chooses to go to restaraunt asap (after depot)
    for i in range(2, len(output_list)):
        output_list[i][1] = 7666432.01
    print(output_list)
    # output data
    return (output_list, addresses)

def create_data_model():
    # create distance matrix; also get corresponding addresses
    distancematrix, addresses = generate_distance_matrix()
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
    plan_output = 'Route for vehicle 0:\n'
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
    plan_output += 'Route distance: {}meters\n'.format(route_distance)
    print(plan_output)
    return plan_output

def main():
    # run ORTools
    addresses, data = create_data_model()
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
        route_solution

    return route_solution

if __name__ == '__main__':
    # run the main script
    main()
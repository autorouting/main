from __future__ import print_function
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

geolocator = Nominatim(user_agent=input("Your app name:\n "))
G = ox.graph_from_place(input("city (ex.: Piedmont, California, USA):\n "), network_type='drive')

addresses = []
locations = []
coords = []
nodes = []

inputfile = open("locations.txt", "r")
inputs = inputfile.read().split("\n")
inputfile.close()

for i in range(len(inputs)):
    addresses.append(inputs[i])
    locations.append(geolocator.geocode(addresses[i]))
    coords.append((locations[i].latitude, locations[i].longitude))
    nodes.append(ox.get_nearest_node(G, coords[i]))

def generate_distance_matrix():
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    output_list[0][1] = 0.07
    return output_list

def create_data_model():
    data = {}
    data['distance_matrix'] = generate_distance_matrix()
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
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
    print(plan_output)
    outputfile = open("route.txt", "w")
    outputfile.write(textfileoutput)
    outputfile.close()
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def main():
    data = create_data_model()
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
    if solution:
        print_solution(manager, routing, solution)

if __name__ == '__main__':
    main()
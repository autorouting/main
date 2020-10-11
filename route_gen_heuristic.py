from __future__ import print_function
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

geolocator = Nominatim(user_agent=input("Your app name:\n "))
G = ox.graph_from_place(input("city (ex.: Piedmont, California, USA):\n "), network_type='drive')
drivers = int(input('How many drivers are there?  '))

addresses = []
locations = []
coords = []
nodes = []

inputfile = open("locations.txt", "r")
inputs = inputfile.read().split("\n")
inputfile.close()

i = 0

while i < len(inputs):
    if inputs[i] == '' or inputs[i] == ' ' or inputs[i] == None:
        inputs.remove(inputs[i])
        i -= 1
        
    i += 1
    
i = 0

for i in range(len(inputs)):
    addresses.append(inputs[i])
    locations.append(geolocator.geocode(addresses[i]))
    while i < len(locations):
        if locations[i] == '' or locations[i] == ' ' or locations[i] == None:
            inputs.remove(locations[i])
            i -= 1
        
        i += 1
    coords.append((locations[i].latitude, locations[i].longitude))
    nodes.append(ox.get_nearest_node(G, coords[i]))

def generate_distance_matrix():
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    for i in range(2, len(output_list)):
        output_list[i][1] = 7666432.01
    return output_list

def create_data_model():
    data = {}
    data['distance_matrix'] = generate_distance_matrix()
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    #print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = ''
    route_distance = 0
    textfileoutput = ""
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        textfileoutput += ' {} ->'.format(addresses[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}'.format(addresses[manager.IndexToNode(index)])
    textfileoutput += ' {}\n'.format(addresses[manager.IndexToNode(index)])
    outputfile = open("route.txt", "w")
    outputfile.write(textfileoutput)
    outputfile.close()
    return plan_output
    
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
        plan_output = print_solution(manager, routing, solution)
        
    plan_output = plan_output.replace(', ', ' ')
    plan_output = plan_output.replace(' -> ', ', ')
    plan_list = list(plan_output.split(', '))
    plan_list[0] = plan_list[0][1:]
    def chunks(l, n):
        return [l[i:i + n] for i in range(0, len(l), n)]
    
    plan_chunks = chunks(plan_list[1:len(plan_list) - 1], round((len(plan_list) - 2) / drivers))
    for i in range(len(plan_chunks)):
        plan_chunks[i].insert(0, plan_list[0])
        
    while len(plan_chunks) > drivers and len(plan_chunks[-1]) > 1:
        j = 0
        if len(plan_chunks[-1]) < 2:
            break
            
        for i in range(1, len(plan_chunks[-1])):
            plan_chunks[j].append(plan_chunks[-1][i])
            j += 1
            j = j % (len(plan_chunks) - 1)
        
        plan_chunks.remove(plan_chunks[-1])
                
        
    print(plan_chunks)
    
    end_points = []
    
    for i in range(drivers):
        end_points.append(input('Where is the drivers home?  '))   
    
    locations = []
    
    for i in range(len(end_points)):
        locations.append(geolocator.geocode(end_points[i]))
    
    if None in locations:
        print("A driver's home address is invalid")
    
    for i in range(len(locations)):    
        coords.append((locations[i].latitude, locations[i].longitude))
        
    plan_chunks_possibilities = []
    for i in range(len(end_points)):
        plan_chunks_possibilities.append(plan_chunks)
    
    for i in range(len(end_points)):
        plan_chunks_possibilities[i][0].append(end_points[i])
        
    print(plan_chunks_possibilities[0])
    
if __name__ == '__main__':
    main()
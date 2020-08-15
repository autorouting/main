from __future__ import print_function
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

geolocator = Nominatim(user_agent=input("Enter user agent email:\n "))
G = ox.graph_from_place(input("city (ex.: Piedmont, California, USA):\n "), network_type='drive')

addresses = []
locations = []
coords = []
nodes = []

inputfile = open("locations.txt", "r")
inputs = inputfile.read().split("\n")
inputfile.close()

driverhomeaddressesfile = open("driver_home_addresses.txt", "r")
driverhomes = driverhomeaddressesfile.read().split("\n")
driverhomeaddressesfile.close()

for i in range(len(driverhomes)):
    try:
        addresses.append(inputs[i])
        locations.append(geolocator.geocode(addresses[i]))
        coords.append((locations[i].latitude, locations[i].longitude))
        nodes.append(ox.get_nearest_node(G, coords[i]))
    except:
        print("faulty input at line " + str(i) + " of driver_home_addresses.txt")
for i in range(len(inputs)):
    try:
        addresses.append(inputs[i])
        locations.append(geolocator.geocode(addresses[i + len(driverhomes)]))
        coords.append((locations[i + len(driverhomes)].latitude, locations[i + len(driverhomes)].longitude))
        nodes.append(ox.get_nearest_node(G, coords[i + len(driverhomes)]))
    except:
        print("faulty input at line " + str(i + len(driverhomes)) + " of locations.txt")

def generate_distance_matrix():
    output_list = []
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    for i in range(len(driverhomes) + 1, len(output_list)):
        output_list[i][1] = 7666432.01
    for i in range(len(driverhomes) + 1):
        output_list[i][1] = 0.07
    return output_list

def create_data_model():
    data = {}
    data['distance_matrix'] = generate_distance_matrix()
    data['num_vehicles'] = len(driverhomes) # the number of inputed driver home addresses
    data['depot'] = len(driverhomes) # let restraunt address be the first item in locations.txt
    return data

def print_solution(data, manager, routing, solution):
    max_route_distance = 0
    file_output = ""
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id + 1)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
            file_output += ' {} ->'.format(addresses[manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {}\n'.format(addresses[manager.IndexToNode(index)])
        file_output += ' {}\n'.format(addresses[manager.IndexToNode(index)])
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    outputfile = open("route.txt", "w")
    outputfile.write(file_output)
    outputfile.close()
    print('Maximum of the route distances: {}m'.format(max_route_distance))




def main():
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        10000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    main()

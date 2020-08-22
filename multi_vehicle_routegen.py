from __future__ import print_function
from geopy.geocoders import Nominatim
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

geolocator = Nominatim(user_agent=input("User email:\n "))
G = ox.graph_from_place(input("City, County, or State (ex.: Chapel Hill, Orange County, North Carolina):\n "), network_type='drive')
# drivers = int(input('How many drivers are there?  '))
driver_home_addresses_file = open("driver_home_addresses.txt", "r")
driver_home_addresses = driver_home_addresses_file.read().split("\n")
driver_home_addresses_file.close()
drivers = len(driver_home_addresses)

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


i = 0
while i < len(locations):
    if locations[i] == None:
        locations.remove(locations[i])
        i -= 1
        
    i += 1
    
i = 0

for i in range(len(locations)):
    coords.append((locations[i].latitude, locations[i].longitude))
    nodes.append(ox.get_nearest_node(G, coords[i]))

def calc_distance_matrix(coords):
    distance_matrix = []
    for i in range(len(coords)):
        distance_matrix.append([])
        for j in range(len(coords)):
            distance_matrix[i].append(0)
            
    for i in range(len(coords)):
        for j in range(len(coords)):     
            x_distance_squared = (coords[i][0] - coords[j][0]) ** 2
            y_distance_squared = (coords[i][1] - coords[j][1]) ** 2
            distance = (x_distance_squared + y_distance_squared) ** 0.5
            distance_matrix[i][j] = distance
            
    return distance_matrix
    
def calc_distance(point1, point2):
    return ((point1[0] - point2[1]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
def generate_distance_matrix():
    output_list = []
    output_list = calc_distance_matrix(coords)
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

def genoutput(chunks_to_display):
    out = ""
    for row in chunks_to_display:
        out = out + "\n" + " -> ".join(row)
    outputfile = open("route.txt", "w")
    outputfile.write(out)
    outputfile.close()
    return "Routes generated:" + out

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
    
    def chunks(l, drivers):
        plan_chunks = []
        for i in range(drivers):
            plan_chunks.append([])
            
        total = sum(data['distance_matrix'][0])
            
        average = total / drivers
        variance = 0.15 * average
        
        for i in range(len(plan_chunks)):
            distance = 0
            counter = 1
            while distance < average + variance and counter < len(l):
                plan_chunks[i].append(l[counter])
                distance += data['distance_matrix'][counter][counter - 1]
                counter += 1
                
            j = 0
            
            while j < len(l):
                if l[j] in plan_chunks[i]:
                    l.remove(l[j])
                    j -= 1
                
                j += 1
                
        return plan_chunks
            
        
    
    plan_chunks = chunks(plan_list[:len(plan_list) - 1], drivers)
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
    
    end_points = []
    
    for item in driver_home_addresses:
        end_points.append(item)
    
    print(end_points)
    
    locations = []
    
    for i in range(len(end_points)):
        locations.append(geolocator.geocode(end_points[i]))
    print(locations)
    i = 0
    
    while i < len(locations):
        if locations[i] == None:
            locations.remove(locations[i])
            i -= 1
            
        i += 1
        
    i = 0
    
    coords = []
    for i in range(len(locations)):    
        coords.append((locations[i].latitude, locations[i].longitude))

    locations1 = []
    for i in range(len(plan_chunks)):
        locations1.append(geolocator.geocode(plan_chunks[i][-1]))
    
    coords1 = []
    
    for i in range(len(locations1)):
        coords1.append((locations1[i].latitude, locations1[i].longitude))
       
    distance_matrix = []
    for i in range(len(coords1)):
        distance_matrix.append([])
        for j in range(len(coords)):
            distance_matrix[i].append(0)
            
    for i in range(len(coords1)):
        for j in range(len(coords)):
            distance_matrix[i][j] = calc_distance(coords1[i], coords[j])
        
    for i in range(len(plan_chunks)):
        print(distance_matrix)
        min_index = distance_matrix[i].index(min(distance_matrix[i]))
        plan_chunks[i].append(end_points[min_index])
        for j in range(len(distance_matrix)):
            distance_matrix[j].remove(distance_matrix[j][min_index])
        end_points.remove(end_points[min_index])
    print(genoutput(plan_chunks))
    
if __name__ == '__main__':
    main()
from __future__ import print_function
from geopy.geocoders import GoogleV3
import networkx as nx
import osmnx as ox
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle

city_name = ""

#if __name__ == '__main__': city_name = input("City, County, or State (choose smallest one that encompasses on locations): ")

def calc_distance_matrix(coords):
    #Creating initial distance matrix with all 0s
    distance_matrix = []
    #Rows
    for i in range(len(coords)):
        distance_matrix.append([])
        #Columns
        for j in range(len(coords)):
            distance_matrix[i].append(0)
           
    for i in range(len(coords)):
        for j in range(len(coords)):     
            #Calculating euclidean distance
            x_distance_squared = (coords[i][0] - coords[j][0]) ** 2
            y_distance_squared = (coords[i][1] - coords[j][1]) ** 2
            distance = (x_distance_squared + y_distance_squared) ** 0.5
            distance_matrix[i][j] = distance
            
    return distance_matrix
    
def calc_distance(point1, point2):
    #returning euclidean distance
    return ((point1[0] - point2[1]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def generate_distance_matrix(coords):
    output_list = []
    #Putting the distance matrix into output list.  Unnecessary.  Will be removed in final version
    output_list = calc_distance_matrix(coords)
    return output_list

def create_data_model(coords):
    #defining data as a dict
    data = {}
    #defining distance matrix
    data['distance_matrix'] = generate_distance_matrix(coords)
    #initializing num_vehicles
    data['num_vehicles'] = 1
    #initializing depot
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution, addresses):
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

def main(api_key):
    #set_env
    addresses, locations, coords, nodes = [],[],[],[]

    geolocator = GoogleV3(api_key=api_key)
        
    #loading graph of orange county
    G = pickle.load(open("graph", "rb"))
    
    #G = ox.graph_from_place(input("City, County, or State (ex.: Chapel Hill, Orange County, North Carolina):\n "), network_type='drive')
    # drivers = int(input('How many drivers are there?  '))
    
    #reading inputs
    driver_home_addresses_file = open("driver_home_addresses.txt", "r")
    driver_home_addresses = driver_home_addresses_file.read().split("\n")
    driver_home_addresses_file.close()
    drivers = len(driver_home_addresses)
    
    inputfile = open("locations.txt", "r")
    inputs = inputfile.read().split("\n")
    inputfile.close()
    
    #adding geocode readable format to locations.  addresses is a helper
    for i in range(len(inputs)):
        addresses.append(inputs[i])
        locations.append(geolocator.geocode(addresses[i]))
    
    #filtering faulty locations
    i = 0
    while i < len(locations):
        if locations[i] == None:
            locations.remove(locations[i])
            i -= 1
            
        i += 1
        
    i = 0
    #converting locations to lattitude and longitude and putting into coords, and putting the nodes into nodes
    for i in range(len(locations)):
        coords.append((locations[i].latitude, locations[i].longitude))
        nodes.append(ox.get_nearest_node(G, coords[i]))
    
    #creating dict of everything
    data = create_data_model(coords)
    #initializing or-tools formatted vars
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                              data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    #creating solution
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
        plan_output = print_solution(manager, routing, solution, addresses)
        
    plan_output = plan_output.replace(', ', ' ')
    plan_output = plan_output.replace(' -> ', ', ')
    plan_list = list(plan_output.split(', '))
    #splitting solution
    def chunks(l, drivers):
        plan_chunks = []
        for i in range(drivers):
            plan_chunks.append([])
        #Setting some varaibles    
        total = sum(data['distance_matrix'][0])
            
        average = total / drivers
        variance = 0.15 * average
        
        for i in range(len(plan_chunks)):
            distance = 0
            counter = 1
            #if the distance of "chunk" is less than the average, continue
            while distance < average + variance and counter < len(l):
                #append locations to the vehicle index of the entire list of routes
                plan_chunks[i].append(l[counter])
                distance += data['distance_matrix'][counter][counter - 1]
                counter += 1
                
            j = 0
            #remove locations already covered to avoid repeats
            while j < len(l):
                if l[j] in plan_chunks[i]:
                    l.remove(l[j])
                    j -= 1
                
                j += 1

        return plan_chunks
    #define plan_chunks 
    plan_chunks = chunks(plan_list[:len(plan_list) - 1], drivers)
    #add starting location to every vehicle route
    for i in range(len(plan_chunks)):
        plan_chunks[i].insert(0, plan_list[0])
    #If there are any extra locations, add them to each route systematically  
    while len(plan_chunks) > drivers and len(plan_chunks[-1]) > 1:
        j = 0
        if len(plan_chunks[-1]) < 2:
            break
        #For every leftover location, append it to the Jth vehicle route   
        for i in range(1, len(plan_chunks[-1])):
            plan_chunks[j].append(plan_chunks[-1][i])
            j += 1
            j = j % (len(plan_chunks) - 1)
        #remove leftover location
        plan_chunks.remove(plan_chunks[-1])
    #create list of driver's home addresses
    end_points = []
    
    for item in driver_home_addresses:
        end_points.append(item)
    #convert addresses to geocode readable form
    locations = []
    
    for i in range(len(end_points)):
        locations.append(geolocator.geocode(end_points[i]))

    i = 0
    #remove Nonetypes
    while i < len(locations):
        if locations[i] == None:
            locations.remove(locations[i])
            i -= 1
            
        i += 1
        
    i = 0
    #convert to coordinates
    coords = []
    for i in range(len(locations)):    
        coords.append((locations[i].latitude, locations[i].longitude))
    #create list of last stops for each driver route
    locations1 = []
    for i in range(len(plan_chunks)):
        locations1.append(geolocator.geocode(plan_chunks[i][-1]))
    #get coordinates for final stops in each driver route
    coords1 = []
    
    for i in range(len(locations1)):
        coords1.append((locations1[i].latitude, locations1[i].longitude))
    #create distance matrix of driver routes to each endpoint 
    distance_matrix = []
    for i in range(len(coords1)):
        #create rows
        distance_matrix.append([])
        for j in range(len(coords)):
            #create columns
            distance_matrix[i].append(0)
            
    for i in range(len(coords1)):
        for j in range(len(coords)):
            distance_matrix[i][j] = calc_distance(coords1[i], coords[j])
    #append the closest endpoint to the last stop in each route to the respective driver route   
    for i in range(len(plan_chunks)):
        #get minimum distance to the last stop in the i th driver route 
        min_index = distance_matrix[i].index(min(distance_matrix[i]))
        plan_chunks[i].append(end_points[min_index])
        #remove to avoid repeats
        for j in range(len(distance_matrix)):
            distance_matrix[j].remove(distance_matrix[j][min_index])
        end_points.remove(end_points[min_index])
    return genoutput(plan_chunks)
    
if __name__ == '__main__':
    main(input("API key:\n "))


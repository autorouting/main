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
import database

def take_inputs(api_key, fakeinputfile):

    try:
        geolocator = gmaps.Client(key=api_key)
        testgeocode = geolocator.geocode("this is to check if the API key is configured to allow Geocoding.")
    except:
        raise ValueError("The following API key may be problematic: " + api_key)

    # get inputs
    inputs = fakeinputfile.split("\n")

    # initiate vars
    G = pickle.load(open("graph", "rb"))
    addresses = []
    osmnodes = []
    faultyAddress = []
    lessThanOneInt = True
    
    # for every line of input, generate location object
    for i in range(0, len(inputs)):
        placeid = database.fetch_placeid(inputs[i])
        if len(placeid) == 0:
            location = geolocator.geocode(inputs[i])
            try:
                if len(location) == 0:
                    raise "errorerrorerror"
                address = location[0]["formatted_address"]
                coordpair = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
                osmnode = ox.get_nearest_node(G, coordpair)

                database.insert_data(inputs[i], location[0]['place_id'], coordpair[0], coordpair[1], address, str(osmnode))
                
                addresses.append(address)
                osmnodes.append(osmnode)
            except:
                if i == 0:
                    faultyAddress.append("<B>Destination Address(es): </B>")
                elif i == 1:
                    faultyAddress.append("<B>Origin Address(es): </B>")
                elif lessThanOneInt:
                    faultyAddress.append("<B>Intermediate Address(es): </B>")
                    lessThanOneInt = False
                faultyAddress.append(inputs[i])
        else:
            out_data = database.fetch_output_data(placeid[0][0])
            addresses.append(out_data[0][1])
            osmnodes.append(int(out_data[0][0]))

    # output data
    return (faultyAddress, addresses, osmnodes, G)

def generate_distance_matrix(nodes, fast_mode_toggled, G):
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first

    output_list = []

    # create 2d array with distances of node i -> node j
        
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
    faultyAddress, addresses, nodes, G = take_inputs(api_key, fakeinputfile)
    if len(faultyAddress) == 0:
        # run ORTools
        distancematrix = generate_distance_matrix(nodes, fast_mode_toggled, G)
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
    print(main(input("API key:\n "), open("locations.txt", "r").read(), True)[0].replace("<br>", "\n").replace("<B>", "\n\t").replace("</B>", "\t").replace("<h1>", "\n\t").replace("</h1>", "\t\n").replace("<p style=\"color:Tomato;\">", " ").replace("</p>", "\t\n"))
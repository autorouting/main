from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import string
import random
import pickle
import numpy as np
import maputil


class BasicRouter():
    """
    The BasicRouter creates a routes using real world address.

    """

    def __init__(self, addresses: list, apikey: str, distancematrixoption=1):
        '''

        Args:
            addresses: list of all addresses (first address is origin, last address is destination)
            apikey: key for google map api, used to get coordinates of addresses
        '''
        self._addresses = addresses.copy()
        self._apikey = apikey

        #Construct self._coordinates
        self._coordinates = maputil.getcoordinate(self._addresses, apikey)

        #Construct distance matrix via Euclidean distance
        self._distancematrix = maputil.getdistancematrix(self._coordinates, option=distancematrixoption)

    def addIntermediateAddress():
        pass

    def routeOneVehicle(self):
        '''

        Returns: the optimized route assuming only the first driver is available

        '''
        data = {
            "distance_matrix": self._distancematrix,
            "num_vehicles": 1,
            "depot": 0
        }
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
        ordered_indeces = self.print_solution(manager, routing, solution, self._addresses)
        if solution:
            ordered_indeces
        route_solution = []
        route_solution_nonformatted = []
        ordered_coords = []
        for x in ordered_indeces:
            route_solution.append(self._addresses[x])
            route_solution_nonformatted.append(self._addresses[x])
            ordered_coords.append(str(self._coordinates[x][0]) + "," + str(self._coordinates[x][1]))
        #end_time = time.perf_counter_ns()
        #print((end_time - start_time) / 10 ** 9)
        return (route_solution, ordered_coords, route_solution_nonformatted, ordered_indeces)
    
    def print_solution(manager, routing, solution, addresses):
        """
        Creates a displayable version of the solution
        
        Parameters:
        routing (): 
        routing ():
        solution ():
        addresses ():
        
        Returns:
        string[]: solution generated by application
        """
        # create ORTools solution
        #print('Objective: {} meters'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = []
        route_distance = 0
        while not routing.IsEnd(index):
            if index:
                plan_output.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            if index:
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output.append(manager.IndexToNode(index))
        return plan_output
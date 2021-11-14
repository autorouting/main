from __future__ import print_function, absolute_import
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from . import basicrouter


class MultiVehicleRouter(basicrouter.BasicRouter):
    #def __init__(self, input_addresses, api_key, num_vehicles, starts, ends, capacities = null, distancematrixoption=1, span_cost_coeff=100):
    def __init__(self, input_addresses, api_key, num_vehicles, starts, ends, distancematrixoption = 1, force_fairness = False, span_cost_coeff=100, capacities:list = None):
        super().__init__(input_addresses, api_key, distancematrixoption)
        self._numvehicles = num_vehicles
        #force_fairness does nothing right now
        self.force_fairness = force_fairness
        self._span_cost_coeff = span_cost_coeff
        self.starts = starts
        self.ends = ends
        if capacities == None:
            self._capacities = [len(input_addresses) for x in range(num_vehicles)]
        else:
            self._capacities = capacities


    def create_data_model(self):
        # initiate ORTools
        data = {}
        data['distance_matrix'] = self._distancematrix
        data['num_vehicles'] = self._numvehicles
        data['starts'] = self.starts
        data['ends'] = self.ends

        data['demands'] = [1 for x in self._addresses]
        data['vehicle_capacities'] = self._capacities

        return (data)

    def get_formatted_output(self, manager, routing, solution):
        '''

        Args:
            data: doesn't seem to be needed, to be removed later
            manager: manager object from Google OR tools
            routing: routing object from Google OR tools
            solution: solution object from Google OR tools

        Returns: a list of routes (represented as ordered indices of addresses) for each vehicle

        '''
        output = [[] for vehicle in range(self._numvehicles)]

        for vehicle_id in range(self._numvehicles):
            index = routing.Start(vehicle_id)
            while not routing.IsEnd(index):
                output[vehicle_id].append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            output[vehicle_id].append(manager.IndexToNode(index))
            
        return output


    def routeMultiVehicle(self):
        '''

        Returns:

        '''

        """Entry point of the program."""
        # Instantiate the data problem.
        data = self.create_data_model()

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['starts'], data['ends'])

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
            999999999999,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(self._span_cost_coeff)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]
        
        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')



        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            ordered_indices = self.get_formatted_output(manager, routing, solution)
            
            route_solution_nonformatted = []
            ordered_coords = []
            route_solution = []
            for i in range(len(ordered_indices)):
                rsn_row = []
                oc_row = []
                for j in ordered_indices[i]:
                    rsn_row.append(self._addresses[j])
                    oc_row.append(self._coordinates[j])
                route_solution_nonformatted.append(rsn_row)
                ordered_coords.append(oc_row)
                route_solution.append(basicrouter.maputil.getmappedaddresses(rsn_row, self._apikey))
            
            self.output = (route_solution_nonformatted, ordered_coords, ordered_indices, route_solution)
            return self.output
        
        else:
            raise Exception('I know what I am doing.  This is intentional!  I did not make any mistakes.')



if __name__ == '__main__':
    #the first argument is just a test case.  change to your liking, but seperate each address with \n

    solve_multi = MultiVehicleRouter("""103 E Main St, Carrboro, NC 27510
    1129 Weaver Dairy Rd, Chapel Hill, NC 27514
    1810 Fordham Blvd, Chapel Hill, NC 27514
    1826 M.L.K. Jr Blvd, Chapel Hill, NC 27514
    790 M.L.K. Jr Blvd, Chapel Hill, NC 27514""".splitlines(), input('API Key: '), 2, [0, 1], [4, 4])
    print(solve_multi.routeMultiVehicle())


from __future__ import print_function
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import basicrouter


class solve_multi(basicrouter.BasicRouter):
    def __init__(self, input_addresses, api_key, num_vehicles, distancematrixoption = 1, force_fairness = False):
        super().__init__(input_addresses, api_key, distancematrixoption)
        self._numvehicles = num_vehicles
        #force_fairness does nothing right now
        self.force_fairness = force_fairness
        
        print('Maximum of the route distances: {}m'.format(max_route_distance))



    def main(self):
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
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            def print_solution(data, manager, routing, solution):
                """Prints solution on console."""
                print(f'Objective: {solution.ObjectiveValue()}')
                max_route_distance = 0
               for vehicle_id in range(data['num_vehicles']):
                    index = routing.Start(vehicle_id)
                    plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                    route_distance = 0
                    while not routing.IsEnd(index):
                        plan_output += ' {} -> '.format(manager.IndexToNode(index))
                        previous_index = index
                        index = solution.Value(routing.NextVar(index))
                        route_distance += routing.GetArcCostForVehicle(
                            previous_index, index, vehicle_id)
                    plan_output += '{}\n'.format(manager.IndexToNode(index))
                    plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                    print(plan_output)
                    max_route_distance = max(route_distance, max_route_distance)
            
            self.print_solution(data, manager, routing, solution)
        
        else:
            print('No solution found!')



if __name__ == '__main__':
    #the first argument is just a test case.  change to your liking, but seperate each address with \n

    solve_multi = solve_multi("""103 E Main St, Carrboro, NC 27510
    1129 Weaver Dairy Rd, Chapel Hill, NC 27514
    1810 Fordham Blvd, Chapel Hill, NC 27514
    1826 M.L.K. Jr Blvd, Chapel Hill, NC 27514
    790 M.L.K. Jr Blvd, Chapel Hill, NC 27514""".splitlines(), input('API Key: '), 2)
    solve_multi.main()

from __future__ import print_function
import googlemaps as gmaps
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import concurrent.futures
import time
import math
import multiprocessing
import requests
from basicrouter import BasicRouter


class solve_multi(BasicRouter):
    def __init__(self, input_addresses, api_key, num_vehicles, fast_mode_toggled, force_fairness = False, max_workers = 2):
        super().__init__(input_addresses, api_key, int(not fast_mode_toggled), True)
        print(1)
        #self.input_addresses = input_addresses
        #self.api_key = api_key
        self.num_vehicles = num_vehicles
        self.fast_mode_toggled = int(not fast_mode_toggled)
        #force_fairness does nothing right now
        self.force_fairness = force_fairness
        self.max_workers = max_workers


    def process_inputs(self):
        try:
            geolocator = gmaps.Client(key = self.api_key)
            testgeocode = geolocator.geocode("This is to check if the API key is configured to allow Geocoding.")
        
        except:
            raise ValueError("The following API key may be problematic: " + self.api_key)
        
        inputs = []

        for line in self.input_addresses.split("\n"):
            if len(line.strip()) > 0:
                inputs.append(line.strip())

        futures = []
        with concurrent.futures.ThreadPoolExecutor(self.max_workers) as executer:
            for address in inputs:
                future = executer.submit(self.geocode_input, address, geolocator)
                futures.append(future)
        
        # Wait until all are finished
        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
        results = [future.result() for future in futures]

        faulty_addresses = []
        addresses = []
        coord_pairs = []
        
        for i in range(len(results)):
            if results[i][1] != None: 
                addresses.append(results[i][1])
                coord_pairs.append(results[i][2])
            
            else:
                faulty_addresses.append(results[i][0]) 
                addresses.append(None)
                coord_pairs.append(None)
        
        self.faulty_addresses = faulty_addresses
        self.addresses = addresses
        self.coord_pairs = coord_pairs
        self.inputs = inputs


    def geocode_input(self, input, geolocator):
        #deleted the database stuff for simplicity for now.  it will be added back later
        faulty_address = None
        address = None
        coords = None
        
        try:
            location = geolocator.geocode(input + " NC") # IMPORTANT: NC must be changed for usage in different states.
            coords = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
            address = location[0]["formatted_address"]

        except:
            faulty_address = str(input)

        return (faulty_address, address, coords, input)


    def create_data_model(self):
        self.data = {}
        self.data['distance_matrix'] = self.distance_matrix(self.coord_pairs, self.fast_mode_toggled)
        self.data['num_vehicles'] = self.num_vehicles
        self.data['depot'] = 0
        #print(self.data)

    """
    def create_distance_matrix(self):
        if self.fast_mode_toggled:
            return self.create_fast_mode_matrix()

        else:
            return self.orsm_distance_matrix
        
    def fast_mode_distance(self, coords1, coords2):
        DEGREE_TO_RAD = 0.017 #this is pi/180
        DEGREE_LATITUDE = 111133 # 1 degree of longitude at the equator, in meters
            # convert coords to meters
        lon1 = coords1[1] * DEGREE_LATITUDE * math.cos(coords1[0] * DEGREE_TO_RAD)
        lon2 = coords2[1] * DEGREE_LATITUDE * math.cos(coords2[0] * DEGREE_TO_RAD)
        lat1 = coords1[0] * DEGREE_LATITUDE
        lat2 = coords2[0] * DEGREE_LATITUDE
        
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
    
    def create_fast_mode_matrix(self):
        MAX_DISTANCE = 9999999 # a constant rigging distance matrix to force the optimizer to go to origin first. 
        # initiate vars
        distance_matrix = []
        # create 2d array with distances of node i -> node j
        for i in range(len(self.coord_pairs)):
            distance_matrix.append([])
            for j in range(len(self.coord_pairs)):
                distance_matrix[i].append(self.fast_mode_distance(self.coord_pairs[i], self.coord_pairs[j]))
            # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
        for i in range(2, len(distance_matrix)):
            distance_matrix[i][1] = MAX_DISTANCE

        return distance_matrix


    def osrm_distance_matrix(self):
        MAX_DISTANCE = 9999999 # a constant rigging distance matrix to force the optimizer to go to origin first
        rstring = "http://router.project-osrm.org/table/v1/driving/"
        coordsstring = []
        
        for coords in self.coord_pairs:
            coordsstring.append(str(coords[1]) + "," + str(coords[0]))
            # lat/long seems to be reversed???
        rstring += ";".join(coordsstring)
        r = requests.get(rstring)
        distance_matrix = r.json()["durations"]
        # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
        for i in range(2, len(distance_matrix)):
            distance_matrix[i][1] = MAX_DISTANCE
        
        return distance_matrix
    
    """
    def print_solution(self, data, manager, routing, solution):
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
        
        print('Maximum of the route distances: {}m'.format(max_route_distance))



    def main(self):
        """Entry point of the program."""
        # Instantiate the data problem.
        data = self.data

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
            self.print_solution(data, manager, routing, solution)
        
        else:
            print('No solution found!')



if __name__ == '__main__':
    #the first argument is just a test case.  change to your liking, but seperate each address with \n

    solve_multi = solve_multi('103 E Main St, Carrboro, NC 27510 \n 1129 Weaver Dairy Rd, Chapel Hill, NC 27514 \n 1810 Fordham Blvd, Chapel Hill, NC 27514 \n 1826 M.L.K. Jr Blvd, Chapel Hill, NC 27514 \n 790 M.L.K. Jr Blvd, Chapel Hill, NC 27514', input('API Key: '), 2, True)
    print(1)
    solve_multi.process_inputs()
    print(2)
    solve_multi.create_data_model()
    print(3)
    solve_multi.main()
    print(4)
    #print(int(True), int(False))
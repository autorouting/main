#Import libraries
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import maputil


class BasicRouter():
    """
    The BasicRouter class allows to find the best route for one vehicle with real world address.

    """

    def __init__(self, addresses: list, apikey: str, distancematrixoption=1):
        '''

        Args:
            addresses: list of all addresses (first address is vehicle's origin, last address is vehicle's final destination)
            apikey: key for google map api, used to get coordinates of addresses
            distancematrixoption: 0 = Euclidean Distances; 1 = Driving Time from OSRM API; 2 = ...
        '''
        self._addresses = addresses.copy()
        self._apikey = apikey
        self._numvehicles = 1
        self._distancematrixoption = distancematrixoption

        #Construct self._coordinates
        self._coordinates = maputil.getcoordinate(self._addresses, apikey)

        #Construct distance matrix via Euclidean distance
        self._distancematrix = maputil.getdistancematrix(self._coordinates, option=distancematrixoption)

        #np.savetxt("foo.csv", np.asarray(self._distancematrix), delimiter=",") # save distance matrix to file

    def addIntermediateAddress(self, address: str):
        """
        
        Args:
            address: string, intermediate address to add to the route
        """
        # Add address to end of addresses
        self._addresses.insert(-1, address)

        #Comment: the current procedure for updating _coordiantes and _distancematrix is inefficient. Can be improved in the future.
        #Remake self._coordinates
        self._coordinates = maputil.getcoordinate(self._addresses, self._apikey)
        
        #Construct distance matrix via Euclidean distance
        self._distancematrix = maputil.getdistancematrix(self._coordinates, option=self._distancematrixoption)
    
    def deleteAddress(self, index: int):
        # Remove address
        self._addresses.pop(index)

        # Remove corresponding coords
        self._coordinates.pop(index)

        # Remove row from distance matrix
        self._distancematrix.pop(index)
        # Column
        for row in self._distancematrix:
            row.pop(index)
    
    def deleteAddresses(self, indices: list):
        for index in sorted(indices, reverse=True):
            self.deleteAddress(index)
    
    def getIndex(self, address: str):
        return self._addresses.index(address)

    def routeOneVehicle(self):
        '''
        Yehua: description of the returns is not accruate
        Returns: the optimized route with a single vehcile
        '''
        data = self.create_data_model()
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                data['num_vehicles'], data['starts'], data['ends'])
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
        
        #Yehua: revisiting this, we are probably better off not have this function but just a few lines of code instead.
        def get_format(manager, routing, solution, addresses):
            """
            Creates a displayable version of the solution
            Args:
                manager:
                routing:
                solution:
                addresses:

            Returns: solution generated by application

            """
            # create ORTools solution
            index = routing.Start(0)
            plan_output = []
            route_distance = 0  #Yehua: route distance seems to be not used.
            while not routing.IsEnd(index):
                plan_output.append(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
            plan_output.append(manager.IndexToNode(index))
            
            return plan_output
        
        ordered_indices = get_format(manager, routing, solution, self._addresses)
        if solution:
            ordered_indices
        route_solution = []
        route_solution_nonformatted = []  #Yehua: I am confused here, route_solution_nonformatted seems to be exactly the same as route solution
        ordered_coords = []
        for x in ordered_indices:
            route_solution.append(self._addresses[x])
            route_solution_nonformatted.append(self._addresses[x])
            ordered_coords.append((self._coordinates[x][0], self._coordinates[x][1]))
        #end_time = time.perf_counter_ns()
        #print((end_time - start_time) / 10 ** 9)

        # Format route_solution
        route_solution = maputil.getmappedaddresses(route_solution, self._apikey)

        self.output = (route_solution, ordered_coords, route_solution_nonformatted, ordered_indices)
        return self.output
    
    def create_data_model(self):
        # initiate ORTools
        """
            Create data for the Google OR Tool
        """
        data = {}
        data['distance_matrix'] = self._distancematrix
        data['num_vehicles'] = self._numvehicles
        data['starts'] = [0]
        data['ends'] = [len(self._distancematrix) - 1]
    
        return (data)

if __name__ == "__main__":
    # This code tests the module
    myRouter = BasicRouter("""li ming’s global market, durham, NC
100 Manora Ln, Chapel Hill, NC 27516
101 Palafox Dr, Chapel Hill, NC 27516
311 Palafox Dr, Chapel Hill, NC 27516
118 Dixie Dr, Chapel Hill, NC 27514
1220 M.L.K. Jr Blvd, Chapel Hill, NC 27514
100 Burnwood Ct, Chapel Hill, NC
390 Erwin Rd, Chapel Hill, NC
532 Lena Cir, Chapel Hill, NC
213 W Franklin St, Chapel Hill, NC 27516""".splitlines(), input("api key???\n > "), distancematrixoption=1)
    #myRouter.addIntermediateAddress("3603 Witherspoon Blvd Suite 101, Durham, NC 27707")
    #myRouter.deleteAddresses([1, 2, 3])
    print(myRouter.getIndex("118 Dixie Dr, Chapel Hill, NC 27514"))
    print(myRouter.routeOneVehicle())

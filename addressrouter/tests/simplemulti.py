from os import path
from addressrouter.multivehiclerouter import MultiVehicleRouter
from addressrouter import maputil


def run_multivehicle(testnum, minmax_coeff=100, capacity: int = None):
    '''

    Args:
        testnum: Index for the multveh_test cases
        minmax_coeff: The coefficient penalize the difference between the and min and max travel time
        capacity: Capacity for each vehicle

    Returns:

    '''
    if path.isfile(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt"):
        # API Key file exists
        pass
    else:
        # Need to make API Key file
        f = open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt", "w")
        f.write(input("API Key????\n > "))
        f.close()

    testfile_read = open(path.dirname(path.abspath(__file__)) + "/testfiles/multiveh_test{}.txt".format(testnum)).read()
    input_addresses = testfile_read.split("###")[0].splitlines()
    num_vehicles = int(testfile_read.split("###\n")[1].splitlines()[0])
    starts = eval("[" + testfile_read.split("###\n")[1].splitlines()[1] + "]")
    ends = eval("[" + testfile_read.split("###\n")[1].splitlines()[2] + "]")

    capacities = None
    if capacity is not None:
        unif_capacities = [capacity for x in range(num_vehicles)]
    myRouter = MultiVehicleRouter(
        input_addresses,
        open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read(),
        num_vehicles,
        starts,
        ends,
        span_cost_coeff=minmax_coeff,
        capacities=unif_capacities
    )
    result = myRouter.routeMultiVehicle()

    # Write outputs to file
    out_file = open(path.dirname(path.abspath(__file__)) + "/testfiles/multiveh_test_output.txt", "w")
    out_file.write(
        " - Test number " + str(testnum) + " - \n"
        + "\nRoute solution:\n\t"
        + "\n\t"
        + str(result)
    )
    out_file.close()

    # Print output
    out_file = open(path.dirname(path.abspath(__file__)) + "/testfiles/multiveh_test_output.txt", "r")
    print(out_file.read())
    out_file.close()

    # Pass on data if needed
    return result


if __name__ == "__main__":
    run_multivehicle(1, minmax_coeff=10)

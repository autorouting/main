from os import path
from addressrouter.multivehiclerouter import MultiVehicleRouter
from addressrouter import maputil

def run_multivehicle(testnum):
    if path.isfile(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt"):
        # API Key file exists
        pass
    else:
        # Need to make API Key file
        f = open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt", "w")
        f.write(input("API Key????\n > "))
        f.close()

    testfile_read = open(path.dirname(path.abspath(__file__)) + "/testfiles/multiveh_test{}.txt".format(testnum)).read()
    myRouter = MultiVehicleRouter(
        testfile_read.split("###")[0].splitlines(),
        open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read(),
        int(testfile_read.split("###\n")[1].splitlines()[0]),
        eval("[" + testfile_read.split("###\n")[1].splitlines()[1] + "]"),
        eval("[" + testfile_read.split("###\n")[1].splitlines()[2] + "]"),
        span_cost_coeff=1000
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
    run_multivehicle(1)
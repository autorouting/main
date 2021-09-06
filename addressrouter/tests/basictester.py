from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+"/src")
from basicrouter import BasicRouter
import maputil

if path.isfile(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt"):
    # API Key file exists
    pass
else:
    # Need to make API Key file
    f = open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt", "w")
    f.write(input("API Key????\n > "))
    f.close()

testnum=2
myRouter = BasicRouter(
    open(path.dirname(path.abspath(__file__)) + "/testfiles/test{}.txt".format(testnum)).read().splitlines(),
    open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read()
)
result = myRouter.routeOneVehicle()

# Write outputs to file
out_file = open(path.dirname(path.abspath(__file__)) + "/testfiles/test_output.txt", "w")
out_file.write(
    " - Test number " + str(testnum) + " - \n"
    + "\nRoute solution:\n\t"
    + "\n\t".join(result[0])
    + "\n\n"
    + "\nMaps link before solve: " + maputil.genmapslink(myRouter._addresses)
    + "\nMaps link after solve : " + maputil.genmapslink(result[0])
)
out_file.close()

# Print output
out_file = open(path.dirname(path.abspath(__file__)) + "/testfiles/test_output.txt", "r")
print(out_file.read())
out_file.close()
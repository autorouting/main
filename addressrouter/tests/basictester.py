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
    open(path.dirname(path.abspath(__file__)) + "/testfiles/test{}.txt".format(testnum)).read().split("%")[0].splitlines(),
    open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read()
)
result = myRouter.routeOneVehicle()
print("\n".format(testnum).join(result[0]))
print(maputil.genmapslink(result[0]))
print(maputil.genmapslink(myRouter._addresses))
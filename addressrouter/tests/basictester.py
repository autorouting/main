from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))+"/src")
from basicrouter import BasicRouter

testnum=2
myRouter = BasicRouter(
    open(path.dirname(path.abspath(__file__)) + "/testfiles/test{}.txt".format(testnum)).read().splitlines(),
    open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read()
)
print("\n:".format(testnum).join(myRouter.routeOneVehicle()[0]))
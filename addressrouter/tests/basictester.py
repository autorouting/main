from shutil import copyfile
from os import path, getcwd
import sys
sys.path.append(path.dirname(getcwd())+"/src")
from basicrouter import BasicRouter

myRouter = BasicRouter(
    open(getcwd() + "/testfiles/test1.txt").read().splitlines(),
    open(getcwd() + "/testfiles/api.txt").read()
)
print("\n".join(myRouter.routeOneVehicle()[0]))
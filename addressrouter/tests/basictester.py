from shutil import copyfile
from os import path, remove
from addressrouter.src.basicrouter import BasicRouter

# couldn't figure out how imports work :(
# srcpath = path.join(path.dirname(path.dirname(__file__)), "src", "basicrouter.py")
# destpath = path.join(path.dirname(__file__), "basicrouter.py")
# copyfile(srcpath, destpath)
# srcpath = path.join(path.dirname(path.dirname(__file__)), "src", "maputil.py")
# destpath = path.join(path.dirname(__file__), "maputil.py")
# copyfile(srcpath, destpath)
# from basicrouter import BasicRouter
# remove(destpath)
# remove(destpath.replace("maputil", "basicrouter"))



myRouter = BasicRouter(
    open(path.dirname(__file__) + "/testfiles/test1.txt").read().splitlines(),
    open(path.dirname(__file__) + "/testfiles/api.txt").read()
)
print("\n".join(myRouter.routeOneVehicle()[0]))
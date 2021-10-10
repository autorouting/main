from os import path
from addressrouter.basicrouter import BasicRouter
import addressrouter.maputil as maputil
import matplotlib.pyplot as plt
import numpy

if path.isfile(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt"):
    # API Key file exists
    pass
else:
    # Need to make API Key file
    f = open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt", "w")
    f.write(input("API Key????\n > "))
    f.close()

testnum=1
myRouter = BasicRouter(
    open(path.dirname(path.abspath(__file__)) + "/testfiles/test{}.txt".format(testnum)).read().split("%")[0].splitlines(),
    open(path.dirname(path.abspath(__file__)) + "/testfiles/api.txt").read()
)
result = myRouter.routeOneVehicle()
print("\n".format(testnum).join(result[0]))
print(maputil.genmapslink(result[0]))
print(maputil.genmapslink(myRouter._addresses))


#ordered coordinates need to be a list of numbers.
#This is currently manually entered, need someone to help to automate this.
#ordered_coordinates = [[35.9661961,-78.963248], [35.9733299,-79.0508445], [35.9445544,-79.0560079], [35.9114138,-79.0590048999999]]
ordered_coordinates = result[1]

x_coordinates = [row[1] for row in ordered_coordinates]
y_coordinates = [row[0] for row in ordered_coordinates]

#specifying the boundaries of the plot
x_min = min(x_coordinates) - numpy.std(x_coordinates)
x_max = max(x_coordinates) + numpy.std(x_coordinates)
y_min = min(y_coordinates) - numpy.std(y_coordinates)
y_max = max(y_coordinates) + numpy.std(y_coordinates)

#plot origin
plt.plot(x_coordinates[0], y_coordinates[0], 'k>', markersize=9)
#plot destination
plt.plot(x_coordinates[-1], y_coordinates[-1], 'k<', markersize=9)
#plot intermediate addresses
plt.plot(x_coordinates[1:len(result[1])-1], y_coordinates[1:len(result[1])-1], 'ko', markersize=4)
#plot the tour using lines
plt.plot(x_coordinates, y_coordinates, color='gray', linestyle='-')

plt.show()
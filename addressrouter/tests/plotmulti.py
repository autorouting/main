import simplemulti
import matplotlib.pyplot as plt
import numpy

testnum = 3
result = simplemulti.run_multivehicle(testnum, minmax_coeff=100, capacity=100)
#result = simplemulti.run_multivehicle(testnum)
#run_multivehicle(1, minmax_coeff=10)

color_spectrum = ["red", "orange", "yellow", "green", "blue", "purple"]
color_index = 0

for ordered_coordinates in result[1]:
    x_coordinates = [row[1] for row in ordered_coordinates]
    y_coordinates = [row[0] for row in ordered_coordinates]

    #plot origin
    plt.plot(x_coordinates[0], y_coordinates[0], 'k*', markersize=9, color=color_spectrum[color_index])
    #plot destination
    plt.plot(x_coordinates[-1], y_coordinates[-1], 'k8', markersize=9, color=color_spectrum[color_index])
    #plot intermediate addresses
    plt.plot(x_coordinates[1:len(ordered_coordinates)-1], y_coordinates[1:len(ordered_coordinates)-1], 'ko', markersize=4, color=color_spectrum[color_index])
    #plot the tour using lines
    plt.plot(x_coordinates, y_coordinates, color=color_spectrum[color_index], linestyle='-')

    # Use a new color for next tour
    color_index += 1
    color_index = color_index % len(color_spectrum)

plt.show()
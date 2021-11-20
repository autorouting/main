import simplemulti
import matplotlib.pyplot as plt
import folium
from os import path
import webbrowser

testnum = 1
veh_capacity = 100 #the maximum capacity for each vehicle
result = simplemulti.run_multivehicle(testnum, minmax_coeff=0, capacity=veh_capacity)

m = folium.Map(location=result[1][0][0], zoom_start=15)

color_spectrum = ["red", "orange", "yellow", "green", "blue", "purple"]
color_index = 0

bounds_list = [] # Sum all of the ordered coords for bounds calculation

for i in range(len(result[1])):
    ordered_coordinates = result[1][i]
    bounds_list += ordered_coordinates
    ordered_addresses = result[0][i]

    # Plot edges
    folium.PolyLine(ordered_coordinates, color=color_spectrum[color_index], weight=6.9, opacity=0.69).add_to(m)

    # Plot start
    folium.Marker(location=ordered_coordinates[0], popup=ordered_addresses[0], icon=folium.Icon(icon="star", color=color_spectrum[color_index])).add_to(m)

    # Plot destination
    folium.Marker(location=ordered_coordinates[-1], popup=ordered_addresses[-1], icon=folium.Icon(icon="stop", color=color_spectrum[color_index])).add_to(m)

    # Use a new color for next tour
    color_index += 1
    color_index = color_index % len(color_spectrum)

m.fit_bounds(bounds_list) # zoom map correctly

map_html = m.get_root().render() # Get map HTML
# Write HTML file
out_file = open(path.dirname(path.abspath(__file__)) + "/testfiles/folium_output.html", "w")
out_file.write(map_html)
out_file.close()

# Open HTML file
webbrowser.open("file://" + path.dirname(path.abspath(__file__)) + "/testfiles/folium_output.html")
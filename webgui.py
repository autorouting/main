#!put your python path here ...\python.exe
import cgi, cgitb
import onevehicleroutegen_web
import genmapslink_web

# get the inputs
form = cgi.FieldStorage()
api_key = form.getvalue("api_key")
driver_address = form.getvalue("driver")
restaurant_address = form.getvalue("restaurant")
consumer_addresses = form.getvalue("consumer")

# Write inputs to communication file
locationstextfile = open("locations.txt", "w")
locationstextfile.write(driver_address + "\n" + restaurant_address + "\n" + consumer_addresses)
locationstextfile.close()

route_solution = onevehicleroutegen_web.main(api_key)
route_link = genmapslink_web.maps_link()

# Display routes
print("Content-type:text/html\n")
print(route_solution.replace(" -> ", " -><br>"))
print("<br/><a target='_blank' href='" + route_link + "'>Open Google Maps link</a>")

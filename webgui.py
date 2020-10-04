import cgi, cgitb
import onevehicleroutegen
import genmapslink

# get the inputs
form = cgi.FieldStorage()
api_key = form.getvalue("api_key")
driver_address = form.getvalue("driver")
restaurant_address = form.getvalue("restaurant")
consumer_addresses = form.getvalue("consumer")

route_solution = onevehicleroutegen.main(api_key)
route_link = genmapslink.maps_link()

print("Content-type:text/html")
print(route_solution.replace(" -> ", " ->\n"))
print("<br/><a href='" + route_link + "'>Open Google Maps link</a>")
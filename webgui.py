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

# change to HTML display
print("Content-type:text/html\n")
print()

# add doc title
print("<title>Autorouting app (Solutions)</title>")

# add stylesheet
print("""
body {
    font-family: Arial, Helvetica, sans-serif;
}
#containerbox {
    border-radius: 5px;
    background-color: #f2f2f2;
    padding: 20px;
    filter: drop-shadow(-0.1px 1px 3px #bbbbbb);
    -webkit-filter: drop-shadow(-0.1px 1px 3px #bbbbbb);
}
""")

route_solution = onevehicleroutegen_web.main(api_key)
route_link = genmapslink_web.maps_link()

# Display routes
print("<div id='containerbox'>"
 + "<b>Route generated:</b><br/>"
 + route_solution.replace(" -> ", " -><br/>")
 + "<br/><a target='_blank' href='" + route_link + "'>Open Google Maps link</a>"
 + "</div>")
#!/usr/bin/python3
import cgi, cgitb
import onevehicleroutegen_web
import genmapslink_web

# get the inputs
form = cgi.FieldStorage()
api_key = form.getvalue("api_key")
driver_address = form.getvalue("driver")
restaurant_address = form.getvalue("restaurant")
consumer_addresses = form.getvalue("consumer")
 
# create big input string
locationstextfilecontent = driver_address + "\n" + restaurant_address + "\n" + consumer_addresses

# change to HTML display
print("Content-type:text/html\n")
print()

# add doc title
print("<title>Autorouting app (Solutions)</title>")

# add stylesheet
print("""<style>
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
</style>""")

route_solution, stringoutput = onevehicleroutegen_web.main(api_key, locationstextfilecontent)
route_link = genmapslink_web.maps_link(-1, stringoutput)

# Display routes
print("<div id='containerbox'>"
 + route_solution.replace(" -> ", " -><br/>")
 + "<br/><br/><a target='_blank' href='" + route_link + "'>Open Google Maps link</a>"
 + "</div>")
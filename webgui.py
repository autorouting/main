#!/usr/bin/python3
import cgi, cgitb
import onevehicleroutegen_web
import genmapslink_web
import urllib

# cgitb.enable() # comment out after usage

# get the inputs
form = cgi.FieldStorage()
api_key = ""# Enter API key here
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
iframe {
    border: 0;
    width: 300px;
    height: 300px;
}
</style>""")

route_solution, stringoutput = onevehicleroutegen_web.main(api_key, locationstextfilecontent)
route_link = genmapslink_web.maps_link(stringoutput, -1)

# Display routes
print("<div id='containerbox'>"
 + route_solution.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(" -> ", " -><br/>")
 + "<a target='_blank' href=\"" + route_link.replace(u"\u2018", "'").replace(u"\u2019", "'") + "\">Open Google Maps link</a>"
 + "<br/>Or scan this QR code:<br/><iframe src=\"https://easyqrgen.netlify.app/index.html?uri=" + urllib.parse.quote_plus(route_link) + "\">oops, something's broken</iframe>"
 + "</div>")
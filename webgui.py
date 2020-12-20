#!/usr/bin/python3

import cgi, cgitb
import onevehicleroutegen_web
import genmapslink_web
import urllib
import send_email
import api_key

"""
Make a file called api_key.py with the following text:
google_geocoding_api = "API_KEY"
"""

cgitb.enable() # comment out after usage

# allow unicode strings
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

# get the inputs
form = cgi.FieldStorage()
driver_address = form.getvalue("driver")
restaurant_address = form.getvalue("restaurant")
consumer_addresses = form.getvalue("consumer")
fast_mode_toggled = form.getvalue("fast_mode_toggled")
user_email = form.getvalue("user_email")
 
# create big input string
locationstextfilecontent = driver_address + "\n" + restaurant_address + "\n" + consumer_addresses

# change to HTML display
print("Content-Type: text/html;charset=utf-8")
print()
print()

# add doc title
print("<title>Autorouting App (Solutions)</title>")

# add stylesheet
stylesheet = open("/var/www/html/delivery/style.css", "r")
print("<style>" + stylesheet.read() + "</style>")
stylesheet.close()

route_solution, stringoutput = onevehicleroutegen_web.main(api_key.google_geocoding_api, locationstextfilecontent, bool(fast_mode_toggled))

if stringoutput != "":
    route_link = genmapslink_web.maps_link(stringoutput, -1)
    
    # read sender and password from email config file
    if str(user_email) != 'None':
        credentials = str(open("email_config.txt", "r").read())
        credentials = credentials.split('\n')
        send_email.send_email_async(credentials[0], credentials[1], user_email, route_link)
    
    # Display routes
    print("<div id='containerbox'>"
    + route_solution.replace(" -> ", " -><br/>")
    + "<br/><a target='_blank' href=\"" + route_link + "\">Open Google Maps link</a>"
    + "<br/>Or scan this QR code:<br/><img src=\"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + urllib.parse.quote_plus(route_link) + "\" />"
    + "</div>")
    
else:
    print(route_solution)

# add translate
print("<div id=\"google_translate_element\"></div><script>function googleTranslateElementInit() { new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element'); }</script><script type=\"text/javascript\" src=\"https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit\"></script>")
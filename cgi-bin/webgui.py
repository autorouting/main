#!/usr/bin/python3

import cgi, cgitb
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
from addressrouter.basicrouter import BasicRouter
from addressrouter import maputil
import send_email
import urllib
import api_key
import json

"""
Make a file called api_key.py with the following text:
google_geocoding_api = "API_KEY"

Calls functions of other files to generate and display optimal route
"""

cgitb.enable(False, "/var/log/apache2/error.log") # Write errors to error log but don't display to users. Replace second argument with your error log file.

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

# change to text display
print("Content-Type: application/json;charset=utf-8")
print()

myRouter = BasicRouter(
    [restaurant_address] + consumer_addresses.split("\n") + [driver_address],
    api_key.google_geocoding_api,
    [1, 0][int(bool(fast_mode_toggled))]
)
route_solution_nonformatted, ordered_coords, numsequence, route_solution = myRouter.routeOneVehicle()

output_dict = {}

if ordered_coords != "":
    route_link = maputil.genmapslink(route_solution)
    
    # read sender and password from email config file
    if str(user_email) != 'None':
        credentials = str(open("email_config.txt", "r").read())
        credentials = credentials.split('\n')
        send_email.send_email_async(credentials[0], credentials[1], user_email, route_link)
    
    # Display routes
    output_dict["status"] = "made_route"
    output_dict["route_solution"] = route_solution
    output_dict["route_solution_nonformatted"] = route_solution_nonformatted
    output_dict["route_link"] = route_link
    output_dict["number_sequence"] = numsequence

    # Dev data
    output_dict["dev_data"] = {}
    unordered = [restaurant_address] + consumer_addresses.split("\n") + [driver_address]
    output_dict["dev_data"]["unordered_maps_link"] = maputil.genmapslink(unordered)
    
else:
    output_dict["status"] = "invalid_address"
    output_dict["errorMessage"] = route_solution
    if str(user_email) != 'None':
        credentials = str(open("email_config.txt", "r").read())
        credentials = credentials.split('\n')
        send_email.send_error_email(credentials[0], credentials[1], user_email, route_solution)

print(json.dumps(output_dict))
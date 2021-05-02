#!/usr/bin/python3

import cgi, cgitb
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE_STATUS_RESPONSE
import onevehicleroutegen_web
import genmapslink_web
import send_email
import urllib
import api_key
import json

"""
Make a file called api_key.py with the following text:
google_geocoding_api = "API_KEY"
"""

cgitb.enable(False, "/var/log/httpd/error_log") # Write errors to error log but don't display to users. Replace second argument with your error log file.

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

# change to text display
print("Content-Type: application/json;charset=utf-8")
print()

route_solution, ordered_coords, route_solution_nonformatted = onevehicleroutegen_web.main(api_key.google_geocoding_api, locationstextfilecontent, fast_mode_toggled)

output_dict = {}

if ordered_coords != "":
    route_link = genmapslink_web.maps_link(" -> ".join(ordered_coords), -1)
    
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

    # Dev data
    output_dict["dev_data"] = {}
    output_dict["dev_data"]["unordered_maps_link"] = genmapslink_web.maps_link(restaurant_address + "\n" + consumer_addresses + "\n" + driver_address).replace("\n", " -> ")
    
else:
    output_dict["status"] = "invalid_address"
    output_dict["errorMessage"] = route_solution
    if str(user_email) != 'None':
        credentials = str(open("email_config.txt", "r").read())
        credentials = credentials.split('\n')
        send_email.send_error_email(credentials[0], credentials[1], user_email, route_solution)

print(json.dumps(output_dict))
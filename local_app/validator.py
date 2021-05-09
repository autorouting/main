from geopy.geocoders import Nominatim
import string
import random

# Generate random Nomaintim Key
def gen_rand_key():
    # adding all lowercase letters to symbols
    symbols = list(string.ascii_lowercase)
    # adding numbers to list of symbols
    for i in range(10):
        symbols.append(str(i))
    
    key = []
    # choose 10 random digits and append them to a list 
    for i in range(10):
        key.append(random.choice(symbols))
    # turn list into string, return it as finished key
    return ''.join(key)

# Create a list of invalid addresses
def validate(addresses):
    out = []

    # try to create geocoder
    while True:
        try:
            geolocator = Nominatim(user_agent = gen_rand_key())
            print("VALIDATOR: created key")
            break # if all goes smoothly, go on
        except:
            joe = "joe" # just to fill in the except; doesn't have real meaning
            # retry key generation
    
    # validate
    for address in addresses:
        if geolocator.geocode(address) == None and address != "":
            out.append(address)
    
    print("VALIDATOR: finished validation process")

    return out
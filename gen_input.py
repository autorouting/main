import webbrowser

inputs = open("addresses.txt", "r")
addresses = inputs.read().split("\n")
inputs.close()

i = 1
for address in addresses:
    webbrowser.open("https://www.google.com/maps/place/whatever the address is".replace("whatever the address is", address), new=i)
    if i == 1:
        i += 1
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random
import onevehicleroutegen
import genmapslink
import webbrowser

# Initiate Tkinter
root = Tk()
root.title("Autorouting app (one-vehicle)")

# Build display
label1 = Label(root, text="Google Geocoding API key:")
label1.pack()

apikeybox = Entry(root, width=50)
apikeybox.pack()

label2 = Label(root, text="Driver address:")
label2.pack()

driveraddressbox = Entry(root, width=50)
driveraddressbox.pack()

label3 = Label(root, text="Restaurant address:")
label3.pack()

restrauntaddressbox = Entry(root, width=50)
restrauntaddressbox.pack()

label4 = Label(root, text="Consumer adresses (separate with line breaks):")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50,height=30)
consumeraddressbox.pack()

# main
def launch():
    global route_solution

    # make new window
    newroot = Tk()
    newroot.title("Solution")

    # Write inputs to communication file
    locationstextfile = open("locations.txt", "w")
    locationstextfile.write(driveraddressbox.get().replace("\n", "") + "\n" + restrauntaddressbox.get().replace("\n", "") + "\n" + consumeraddressbox.get('1.0', END))
    locationstextfile.close()

    # Save value before destroying all widgets
    apikey = apikeybox.get()

    # Communicate with main program
    route_solution = onevehicleroutegen.main(apikey)

    # Generate output text
    display_route = Label(newroot, text=route_solution.replace(" -> ", " ->\n"))
    display_route.pack()

    # Generate output link
    route_link = genmapslink.maps_link()
    def callback():
        webbrowser.open(route_link, 0) # open link in browser if callback is called

    button_link = Button(newroot, text="Open Google Maps link in browser", command=callback)
    button_link.pack()

    newroot.mainloop()

# Finish main display
myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

root.mainloop() # required for Tkinter
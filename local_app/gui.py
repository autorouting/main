from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random
import onevehicleroutegen
import genmapslink
import webbrowser
import api_key

# Initiate Tkinter
root = Tk()
root.title("Autorouting app (one-vehicle)")

# Build display
label3 = Label(root, text="Starting address:")
label3.pack()

restrauntaddressbox = Entry(root, width=50)
restrauntaddressbox.pack()

label4 = Label(root, text="Intermediate addresses (one address per line)")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50,height=30)
consumeraddressbox.pack()

label2 = Label(root, text="Ending address:")
label2.pack()

driveraddressbox = Entry(root, width=50)
driveraddressbox.pack()

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

    # Communicate with main program
    route_solution = onevehicleroutegen.main(api_key.google_geocoding_api)

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

# Github link
def open_repo(useless_parameter):
    webbrowser.open_new_tab("https://github.com/autorouting/main")
bottomtext = Label(root, text="Fork us on Github!", fg="blue", cursor="hand2")
bottomtext.pack()
bottomtext.bind("<Button-1>", open_repo)

root.mainloop() # required for Tkinter
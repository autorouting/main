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

    # Write inputs to communication file
    locationstextfile = open("locations.txt", "w")
    locationstextfile.write(driveraddressbox.get().replace("\n", "") + "\n" + restrauntaddressbox.get().replace("\n", "") + "\n" + consumeraddressbox.get('1.0', END))
    locationstextfile.close()

    # Destroy previous display
    for widget in root.winfo_children():
        widget.destroy()
    loading = Label(root, text="Loading...")
    loading.pack()

    # Communicate with main program
    route_solution = onevehicleroutegen.main()
    for widget in root.winfo_children():
        widget.destroy()

    # Generate output text
    display_route = Label(root, text=route_solution.replace(" -> ", " ->\n"))
    display_route.pack()

    # Generate output link
    route_link = genmapslink.maps_link()
    def callback():
        webbrowser.open(route_link, 0) # open link in browser if callback is called

    button_link = Button(root, text="Open Google Maps link in browser", command=callback)
    button_link.pack()

# Finish main display
myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

root.mainloop() # required for Tkinter
# [START import]
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import random
import multi_vehicle_routegen as mvr
import webbrowser
import genmapslink
from functools import partial
import validator
import api_key
# [END import]

#How to setup API Key button
def displayAPI():
    webbrowser.open("apikeysetupguide.html")

def yes():
    global endpoint
    global label6
    endpoint = no
    label6 = Label(root, text="Please input number of drivers and leave ending addresses blank")
    label6.pack()
def no():
    global endpoint
    global label6
    endpoint = yes
    label6 = Label(root, text="Please input ending addresses and leave number of drivers blank")
    label6.pack()
    
#Verify if textboxes on the gui are empty or not
def validate():
    if restaurantaddressbox.get()=="" or len(driveraddressbox.get("1.0", END)) == 0 or len(consumeraddressbox.get("1.0", END))== 0: return False
    else: return True

#Launch routing 
def launch():
    """
    #Check for faulty addresses
    if endpoint == yes:
        faultyaddresses = validator.validate(driveraddressbox.get("1.0", END).split("\n") + restaurantaddressbox.get().split("\n") + consumeraddressbox.get('1.0', END).split("\n"))
    if endpoint == no:
        faultyaddresses = validator.validate(restaurantaddressbox.get().split("\n") + consumeraddressbox.get('1.0', END).split("\n") + list(num_drivers.get()))
    """ # this framework currently doesn't work on latest versions

    #if all information are provided, proceed with distances calculating
    if validate():
        global activation
        activation = [True]
        if len(driveraddressbox.get("1.0", END).strip()) > 0:
            driveroutput = driveraddressbox.get("1.0", END)

        newroot = Tk()
        newroot.title("Solution")

        if len(driveraddressbox.get("1.0", END).strip()) <= 0:
            driveroutput = ''
            for i in range(int(num_drivers.get())):
                driveroutput = driveroutput + restaurantaddressbox.get() + "\n"

        while driveroutput[-1] in ["\n","\t","r"]: driveroutput = driveroutput[:-1]
        consumeroutput = consumeraddressbox.get("1.0", END)
        while consumeroutput[-1] in ["\n","\t","r"]: consumeroutput = consumeroutput[:-1]
        #save driver
        with open("driver_home_addresses.txt", "w") as drivertextfile: drivertextfile.write(driveroutput)
        
        #save api key
        apikey = api_key.google_geocoding_api

        #save consumer
        with open("locations.txt", "w") as locationstextfile: locationstextfile.write(restaurantaddressbox.get().replace("\n", "") + "\n" + consumeroutput)
        """
        for widget in root.winfo_children():
            widget.destroy()
        loading = Label(root, text="Loading...")
        loading.pack()
        for widget in root.winfo_children():
            widget.destroy()
        """
        def callback(routelink):
            global activation
            if activation[0]: webbrowser.open(routelink, 0)

        buttons = []
        displayroutes = []
        functions = [None]
        routes = mvr.main(apikey)
        """
        for widget in root.winfo_children():
            widget.destroy()
        """
        outputroutes = routes.split("\n")
        for outputting in range(len(outputroutes)):
            displayroutes.append(Label(newroot, text=(outputroutes[outputting].replace("\n", "\n\n")).replace(" -> ", " ->\n")))
            displayroutes[-1].pack()
            if outputting != 0:
                print(partial(genmapslink.maps_link, outputting)())
                buttons.append(Button(newroot, text="Open Google Maps link in browser", command=partial(callback, partial(genmapslink.maps_link, outputting)())))
                buttons[-1].pack()
                #pad empty space between objects
                labelSpace = Label(newroot, pady=5)
                labelSpace.pack()
        activation[0] = True

        newroot.mainloop()
            
    #if any input box is empty, display a message box     
    else:
        messagebox.showwarning(title="Warning", message="Please fill in every box.")

# [START input form objects]
# These are labels and textboxes on the GUI input form.
root = Tk()
root.title("Autorouting app")

label2 = Label(root, text="Starting address:")
label2.pack()

restaurantaddressbox = Entry(root, width=50)
restaurantaddressbox.pack()

label4 = Label(root, text="Intermediate addresses:")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50,height=8)
consumeraddressbox.pack()

label2 = Label(root, text="If you would like to end all routes at the starting address, \nenter number of drivers and leave ending addresses blank.\nOtherwise, enter ending addresses and leave number of drivers blank.")
label2.pack()


label3 = Label(root, text="Ending addresses:")
label3.pack()

driveraddressbox = ScrolledText(root, width=50, height = 8)
driveraddressbox.pack()

label5 = Label(root, text="Number of drivers:")
label5.pack()
num_drivers = Entry(root, width=50)
num_drivers.pack()

myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

# Github link
def open_repo(useless_parameter):
    webbrowser.open_new_tab("https://github.com/autorouting/main")
bottomtext = Label(root, text="Fork us on Github!", fg="blue", cursor="hand2")
bottomtext.pack()
bottomtext.bind("<Button-1>", open_repo)
# [END input form objects]

# call the main function
root.mainloop()

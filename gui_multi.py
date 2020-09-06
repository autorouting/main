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
# [END import]

# [START input form objects]
# These are labels and textboxes on the GUI input form.
root = Tk()
root.title("Autorouting app")

label2 = Label(root, text="Restaurant address:")
label2.pack()

restaurantaddressbox = Entry(root, width=50)
restaurantaddressbox.pack()

label3 = Label(root, text="Driver addresses:")
label3.pack()

driveraddressbox = ScrolledText(root, width=50, height = 12)
driveraddressbox.pack()

label4 = Label(root, text="Consumer adresses:")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50,height=12)
consumeraddressbox.pack()
# [END input form objects]

#Verify if textboxes on the gui are empty or not
def validate():
    if restaurantaddressbox.get()=="" or len(driveraddressbox.get("1.0", END)) == 0 or len(consumeraddressbox.get("1.0", END))== 0: return False
    else: return True

#Launch routing
def launch():
    #Check for faulty addresses
    faultyaddresses = validator.validate(driveraddressbox.get("1.0", END).split("\n") + restaurantaddressbox.get().split("\n") + consumeraddressbox.get('1.0', END).split("\n"))

    #if all information are provided, proceed with distances calculating
    if validate() and len(faultyaddresses) == 0:
        global activation
        activation = [True]
        driveroutput = driveraddressbox.get("1.0", END)
        while driveroutput[-1] in ["\n","\t","r"]: driveroutput = driveroutput[:-1]
        consumeroutput = consumeraddressbox.get("1.0", END)
        while consumeroutput[-1] in ["\n","\t","r"]: consumeroutput = consumeroutput[:-1]
        #save driver
        with open("driver_home_addresses.txt", "w") as drivertextfile: drivertextfile.write(driveroutput)
        
        #save consumer
        with open("locations.txt", "w") as locationstextfile: locationstextfile.write(restaurantaddressbox.get().replace("\n", "") + "\n" + consumeroutput)
        for widget in root.winfo_children():
            widget.destroy()
        loading = Label(root, text="Loading...")
        loading.pack()
        for widget in root.winfo_children():
            widget.destroy()
        def callback(routelink):
            global activation
            if activation[0]: webbrowser.open(routelink, 0)
        buttons = []
        displayroutes = []
        functions = [None]
        routes = mvr.main()
        for widget in root.winfo_children():
            widget.destroy()
        outputroutes = routes.split("\n")
        for outputting in range(len(outputroutes)):
            displayroutes.append(Label(root, text=(outputroutes[outputting].replace("\n", "\n\n")).replace(" -> ", " ->\n")))
            displayroutes[-1].pack()
            if outputting != 0:
                print(partial(genmapslink.maps_link, outputting)())
                buttons.append(Button(root, text="Open Google Maps link in browser", command=partial(callback, partial(genmapslink.maps_link, outputting)())))
                buttons[-1].pack()
        activation[0] = True
            
    #if any input box is empty, display a message box     
    elif len(faultyaddresses) == 0:
        messagebox.showwarning(title="Warning", message="Please fill in every box.")
    
    #display faulty addresses
    else:
        messagebox.showwarning(title="Warning", message="The following locations could not be found:\n" + "\n".join(faultyaddresses))

# [START buttons on the input form]
myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()
# [END buttons on the input form]

# call the main function
root.mainloop()

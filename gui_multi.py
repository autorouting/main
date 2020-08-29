from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import random
import multi_vehicle_routegen as mvr
import webbrowser
import genmapslink
root = Tk()
root.title("Autorouting app")

label1 = Label(root, text="City, County, or State:")
label1.pack()

citybox = Entry(root, width=50)
citybox.pack()

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

def validate():
    if citybox.get() == "" or restaurantaddressbox.get()=="" or len(driveraddressbox.get("1.0", END)) == 0 or len(consumeraddressbox.get("1.0", END))== 0: return False
    else: return True

def launch():
    if validate():
        global activation
        activation = [False]
        driveroutput = driveraddressbox.get("1.0", END)
        while driveroutput[-1] in ["\n","\t","r"]: driveroutput = driveroutput[:-1]
        consumeroutput = consumeraddressbox.get("1.0", END)
        while consumeroutput[-1] in ["\n","\t","r"]: consumeroutput = consumeroutput[:-1]
        #save driver
        with open("driver_home_addresses.txt", "w") as drivertextfile: drivertextfile.write(driveroutput)
        
        #save consummer
        with open("locations.txt", "w") as locationstextfile: locationstextfile.write(restaurantaddressbox.get().replace("\n", "") + "\n" + consumeroutput)
        mvr.city_name = citybox.get()
        for widget in root.winfo_children():
            widget.destroy()
        loading = Label(root, text="Loading...")
        loading.pack()
        for widget in root.winfo_children():
            widget.destroy()
        def callback(routelink):
            print("hey")
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
            #def DIE(): callback(genmapslink.maps_link(outputting))
            if outputting != 0:
                buttons.append(Button(root, text="Open Google Maps link in browser", command=callback(genmapslink.maps_link(outputting))))
                buttons[-1].pack()
        activation[0] = True
            
        
    else: messagebox.showwarning(title="Warning", message="Please fill in every box.")

myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

root.mainloop()

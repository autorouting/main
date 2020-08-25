from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import random
import multi_vehicle_routegen as mvr

root = Tk()
root.title("Autorouting app")

label1 = Label(root, text="City:")
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
        #save driver
        with open("driver_home_addresses.txt", "w") as drivertextfile: drivertextfile.write(driveraddressbox.get("1.0", END)[:-1])
        
        #save consummer
        with open("locations.txt", "w") as locationstextfile: locationstextfile.write(restaurantaddressbox.get().replace("\n", "") + "\n" + consumeraddressbox.get('1.0', END)[:-1])
        mvr.city_name = citybox.get()
        loading = Label(root, text="Loading...")
        loading.pack()
        for widget in root.winfo_children():
            widget.destroy()
        #code_to_exec = open("onevehicleroutegen.py").read().replace('input("city (ex.: Piedmont, California, USA):\\n ")', "'" + city + "'").replace('input("Your app name:\\n ")', "'" + str(random.randint(0, 999)) + str(random.randint(0, 999)) + "'") + "\n    exec(open('genmapslink.py').read())"
        #exec(code_to_exec)
        mvr.main()
    else: messagebox.showwarning(title="Warning", message="Please fill in every box.")

myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

root.mainloop()

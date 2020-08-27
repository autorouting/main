from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random
import onevehicleroutegen

root = Tk()
root.title("Autorouting app (one-vehicle)")

label1 = Label(root, text="City:")
label1.pack()

citybox = Entry(root, width=50)
citybox.pack()

label2 = Label(root, text="Driver address:")
label2.pack()

driveraddressbox = Entry(root, width=50)
driveraddressbox.pack()

label3 = Label(root, text="Restraunt address:")
label3.pack()

restrauntaddressbox = Entry(root, width=50)
restrauntaddressbox.pack()

label4 = Label(root, text="Consumer adresses (separate with line breaks):")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50,height=30)
consumeraddressbox.pack()

def launch():
    global route_solution
    locationstextfile = open("locations.txt", "w")
    locationstextfile.write(driveraddressbox.get().replace("\n", "") + "\n" + restrauntaddressbox.get().replace("\n", "") + "\n" + consumeraddressbox.get('1.0', END))
    locationstextfile.close()
    city = citybox.get()
    for widget in root.winfo_children():
        widget.destroy()
    loading = Label(root, text="Loading...")
    loading.pack()
    #code_to_exec = open("onevehicleroutegen.py").read().replace('input("city (ex.: Piedmont, California, USA):\\n ")', "'" + city + "'").replace('input("Your app name:\\n ")', "'" + str(random.randint(0, 999)) + str(random.randint(0, 999)) + "'") + "\n    exec(open('genmapslink.py').read())"
    #exec(code_to_exec)

    route_solution = onevehicleroutegen.main(str(city))
    for widget in root.winfo_children():
        widget.destroy()
    display_route = Label(root, text=route_solution)
    display_route.pack()


myButton = Button(root, text="Launch program", command=launch)
myButton.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

root.mainloop()

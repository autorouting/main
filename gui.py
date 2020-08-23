from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random

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

label4 = Label(root, text="Paste consumer addresses below:")
label4.pack()

consumeraddressbox = ScrolledText(root, width=50, height=30)
consumeraddressbox.pack()

bottomtext = Label(root, text="Find us on GitHub: https://github.com/autorouting/main")
bottomtext.pack()

def onclick():
    locationstextfile = open("locations.txt", "w")
    locationstextfile.write(driveraddressbox.get() + "\n" + restrauntaddressbox.get() + "\n" + consumeraddressbox.get('1.0', END))
    locationstextfile.close()
    city = citybox.get()
    for widget in root.winfo_children():
        widget.destroy()
    loading = Label(root, text="Loading...")
    loading.pack()
    exec(open("onevehicleroutegen.py").read().replace('input("city (ex.: Piedmont, California, USA):\\n ")', "'" + city + "'").replace('input("Your app name:\\n ")', "'" + str(random.randint(0, 999)) + str(random.randint(0, 999)) + "'") + "\n    exec(open('genmapslink.py').read())")

myButton = Button(root, text="Launch program", command=onclick)
myButton.pack()

root.mainloop()
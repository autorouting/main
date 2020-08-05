exec(open("onevehicleroutegen.py").read())
in_file = open("route.txt", "r")
route = in_file.read().split(" -> ")
# route is a text file in the same format as printed from the program
in_file.close()
outstring = "https://www.google.com/maps/dir/"
for i in range(len(route)):
    outstring += route[i].replace(" ", "+") + "/"
print(outstring)
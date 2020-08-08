exec(open("onevehicleroutegen.py").read())
in_file = open("route.txt", "r")
routes = in_file.read().split("\n")
# route is a text file in the same format as printed from the program
in_file.close()
for i in range(len(routes)):
    if routes[i] != "" and routes[i] != " ":
        route = routes[i].split(" -> ")
        outstring = "https://www.google.com/maps/dir/"
        for i in range(len(route)):
            outstring += route[i].replace(" ", "+") + "/"
    print("\nGoogle Maps link for vehicle {}: {}\n".format(i, outstring))

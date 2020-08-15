exec(open("onevehicleroutegen.py").read())
in_file = open("route.txt", "r")
routes = in_file.read().split("\n")
in_file.close()
for i in range(len(routes)):

    if routes[i] != "" and routes[i] != " ":
        route = routes[i].split(" -> ")
        outstring = "https://www.google.com/maps/dir/"
        for j in range(len(route)):
            outstring += route[j].replace(" ", "+") + "/"
        print("\nGoogle Maps link for vehicle {}: {}\n".format(i, outstring))

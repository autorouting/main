#exec(open("onevehicleroutegen.py").read())
def maps_link():
    in_file = open("route.txt", "r")
    routes = in_file.read().split("\n")
    in_file.close()
    
    for i in range(len(routes)):

        if routes[i] != "" and routes[i] != " " and routes[i] != None:
            route = routes[i].split(" -> ")
            outstring = "https://www.google.com/maps/dir/"
            for j in range(len(route)):
                outstring += route[j].replace(" ", "+") + "/"
    output = "Google Maps link for vehicle {}: {}\n".format(i, outstring)
    print(output)
    return outstring
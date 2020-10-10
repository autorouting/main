#exec(open("onevehicleroutegen.py").read())
def maps_link(x=-1):
    in_file = open("route.txt", "r")
    routes = in_file.read().split("\n")
    in_file.close()
    
    outstring = "https://www.google.com/maps/dir/"
    if x==-1:
        for i in range(len(routes)):

            if routes[i] != "" and routes[i] != " " and routes[i] != None:
                route = routes[i].split(" -> ")
                for j in range(len(route)):
                    outstring += route[j].replace(" ", "+") + "/"
                output = "Google Maps link for vehicle {}: {}\n".format(i, outstring)

    else:
        if routes[x] != "" and routes[x] != " " and routes[x] != None:
            route = routes[x].split(" -> ")
            for j in range(len(route)):
                outstring += route[j].replace(" ", "+") + "/"
            output = "Google Maps link for vehicle {}: {}\n".format(x, outstring)
    return outstring
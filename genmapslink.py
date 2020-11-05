import urllib

#exec(open("onevehicleroutegen.py").read())
def maps_link(x=-1):
    in_file = open("route.txt", "r")
    routes = in_file.read().split("\n")
    in_file.close()
    if x==-1:
        for i in range(len(routes)):

            if routes[i] != "" and routes[i] != " " and routes[i] != None:
                route = routes[i].split(" -> ")
                outstring = "https://www.google.com/maps/dir/"
                for j in range(len(route)):
                    outstring += urllib.parse.quote_plus(route[j]) + "/"
                output = "Google Maps link for vehicle {}: {}\n".format(i, outstring)

    else:
        if routes[x] != "" and routes[x] != " " and routes[x] != None:
            route = routes[x].split(" -> ")
            outstring = "https://www.google.com/maps/dir/"
            for j in range(len(route)):
                outstring += urllib.parse.quote_plus(route[j]) + "/"
            output = "Google Maps link for vehicle {}: {}\n".format(x, outstring)
    print(output)
    return outstring

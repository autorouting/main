import urllib

#exec(open("onevehicleroutegen.py").read())
def maps_link(routesstring, x=-1):
    """
    Create google maps link of route

    Parameters:
    routesstring (string): The route generate by app

    Returns:
    string: The google maps link of the route.
    """
    routes = routesstring.split("\n")
    
    outstring = "https://www.google.com/maps/dir/"
    if x==-1:
        for i in range(len(routes)):

            if routes[i] != "" and routes[i] != " " and routes[i] != None:
                route = routes[i].split(" -> ")
                for j in range(len(route)):
                    outstring += urllib.parse.quote_plus(route[j]) + "/"
                output = "Google Maps link for vehicle {}: {}\n".format(i, outstring)

    else:
        if routes[x] != "" and routes[x] != " " and routes[x] != None:
            route = routes[x].split(" -> ")
            for j in range(len(route)):
                outstring += urllib.parse.quote_plus(route[j]) + "/"
            output = "Google Maps link for vehicle {}: {}\n".format(x, outstring)
    return outstring
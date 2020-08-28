import pickle
import osmnx as ox
G = ox.graph_from_place(input("place of which to generate graph (ex.: Orange County, NC, USA):\n "), network_type='drive')
pickle.dump(G, open("graph", "wb"))
print("process completed")
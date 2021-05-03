import pickle
import osmnx as ox
point = (35.8972385, -78.8627028)
streets_graph = ox.graph.graph_from_point(point, dist=80467.2, network_type='drive', simplify=False)
pickle.dump(streets_graph, open("graph", "wb"))
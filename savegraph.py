import osmnx as ox
import pickle

def export_graph(filename, place_to_export):
    G = ox.graph_from_place(place_to_export, network_type='drive')
    hashmap = {"graph": G}
    pickle.dump(hashmap, open(filename, "wb"))

def read_graph(filename):
    hashmap = pickle.load(open(filename, "rb"))
    return hashmap['graph']

if __name__ == "__main__":
    export_graph("graph.p", input("place from which to export graph? (city or county recommended)\n : "))
    print(read_graph("graph.p"))
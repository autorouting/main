import networkx as nx

def generate_distance_matrix(nodes, G):
    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first
    # initiate vars
    output_list = []
    # create 2d array with distances of node i -> node j
    for i in range(len(nodes)):
        output_list.append([])
        for j in range(len(nodes)):
            output_list[i].append(nx.shortest_path_length(G, nodes[i], nodes[j], weight='length'))
    # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
    for i in range(2, len(output_list)):
        output_list[i][1] = MAX_DISTANCE
    # output data
    return (output_list)
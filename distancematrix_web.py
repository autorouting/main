# THIS IS THE CODE THAT CONSTANTLY RUNS IN THE BACKGROUND ON THE SERVER.

import sys
import time
import pickle
import distancematrix_web
import networkx as nx
import osmnx as ox
import serialize
import socket

# Read graph file
G = pickle.load(open('graph', 'rb'))

def generate_distance_matrix(coordpairs, G):
    # get nodes
    nodes = []

    start_time = time.perf_counter()
    
    for coords in coordpairs:
        nodes.append(ox.get_nearest_node(G, coords))

    end_time = time.perf_counter()
    print("Nodes generation time: " + str(end_time - start_time))

    start_time = time.perf_counter()

    MAX_DISTANCE = 7666432.01 # a constant rigging distance matrix to force the optimizer to go to origin first
    # initiate vars
    output_list = [[None for j in range(len(nodes))] for i in range(len(nodes))]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            #assumes i -> j is equal to j -> i
            if output_list[i][j] == None:
                output_list[j][i] = nx.shortest_path_length(G, nodes[j], nodes[i], weight='length')
 
            else:
                output_list[j][i] = output_list[i][j]
    # rig distance so that optimization algorithm chooses to go to origin asap (after depot)
    for i in range(2, len(output_list)):
        output_list[i][1] = MAX_DISTANCE
    # output data

    end_time = time.perf_counter()
    print("Distance calculation time: " + str(end_time - start_time))

    return (output_list)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 6000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        received = b''

        start_time = time.perf_counter()
    
        while True:
            print('start recieving')
            data = connection.recv(256)
            print(data)
            received += data
            if len(data)<256 or data[-1]==10 :
                print('received "%s"' % data)
                break

        end_time = time.perf_counter()
        print("Recieve message time: " + str(end_time - start_time))
            
        #time.sleep(1)
        print("send reply")
        message=generate_distance_matrix(serialize.deserializeCgiToServer(received), G)

        start_time = time.perf_counter()
    
        connection.sendall(serialize.serializeServerToCgi(message))
        print("done sending")

        end_time = time.perf_counter()
        print("Send message time: " + str(end_time - start_time))

    except Exception as err:
        print(err)
            
    finally:
        # Clean up the connection
        print("close socket")
        connection.close()

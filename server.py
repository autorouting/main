import socket
import sys
import time
import pickle
import distancematrix_web

# Read graph file
G = pickle.load(open('graph', 'rb'))

def handle_message(message):
    global G
    coorpairs = message.split(';') # '3,1;1,3' -> ['3,1', '1,3']
    for each in coorpairs: # ['3,1', '1,3'] -> [[3, 1], [1, 3]]
        each = [float(each.split(',')[0]), float(each.split(',')[1])]
    return str(distancematrix_web.generate_distance_matrix(coorpairs, G))

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
        message=''
        while True:
            data = connection.recv(256)
            print('received "%s"' % data)
            message=message+data.decode("utf-8")
            if len(data)<256 or data[-1]==10 :
                print("done: ", message)
                break
        time.sleep(1)
        print("send reply")
        message=handle_message(message)
        connection.sendall(message.encode("utf-8"))
        print("done sending")
            
    finally:
        # Clean up the connection
        print("close socket")
        connection.close()

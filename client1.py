import socket
import sys

def senddata(message):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 6000)
    #print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Send data
        #print('sending "%s"' % message)
        sock.sendall(message)
        #print('done sending')

        # Wait for the response
        received = b''
        while True:
            data = sock.recv(8)
            received += data
            if len(data)<8 or data[-1]==10 :
                #print('received "%s"' % data)
                break
                
        return received
    
    finally:
        print('closing socket')
        sock.close()

if __name__ == '__main__':
    for i in range(10):
        print(senddata('hi this is message ' + str(i)))
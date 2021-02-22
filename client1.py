import socket
import sys

for i in range(0,10):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 6000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Send data
        message = 'client1 This is the message%d. It will be repeated.\n' % (i)
        print('sending "%s"' % message)
        sock.sendall(message.encode('utf-8'))
        print('done sending')

        # Wait for the response
        while True:
            data = sock.recv(256)
            if len(data)<256 or data[-1]==10 :
                print('received "%s"' % data)
                break

    finally:
        print('closing socket')
        sock.close()

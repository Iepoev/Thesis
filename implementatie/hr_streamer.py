import socket
import struct
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# create an INET, STREAMing socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  # bind the socket to a public host, and a well-known port
  s.bind((HOST, PORT))
  # become a server socket
  s.listen(1)

  while True:
    # accept connections from outside
    (clientsocket, address) = s.accept()

    with open('stream') as fp:
      for line in fp:
        clientsocket.send(line.encode('utf8'))
        print("line:", line)
        time.sleep(int(line) / 1000.0) #
      clientsocket.send("eof".encode('utf8'))

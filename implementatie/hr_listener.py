#!/usr/bin/env python3
import struct
import socket
import queue

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
window = []

resting_hr = 220
max_hr = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  data = s.recv(1024)

  while data != "eof".encode('utf8'):
    num = int(data.decode('utf8'))
    window.append(num)

    if len(window) == 10:
      current_hr = (60000 / (sum(window)/len(window)))
      if current_hr < resting_hr:
        resting_hr = current_hr
      if current_hr > max_hr:
        max_hr = current_hr
      window.pop(0)
      print('current HR {0}; current resting HR {1}; current max HR {2}'.format((60000/num), resting_hr, max_hr))
    else:
      print('Heartbeat interval {0}ms'.format(num))

    data = s.recv(1024)



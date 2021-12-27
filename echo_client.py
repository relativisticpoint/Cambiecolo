#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    i=input("entrez le message !") #ligne rajoutée
    i=bytes(i, 'utf-8') #ligne que j ai rajoutée pour envoyer un message personnalisé
    s.sendall(i)
    data = s.recv(63)

print('Received', repr(data))
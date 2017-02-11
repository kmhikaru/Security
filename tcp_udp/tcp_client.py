# -*- coding:utf-8 -*-

import socket

#target_host = "www.google.com"
#target_port = 80

target_host = "0.0.0.0"
target_port = 9999

# instantiate socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
client.connect((target_host, target_port))

# send data
#client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
client.send("GET / HTTP/1.1\r\nHost: 0.0.0.0\r\n\r\n")

# receive data
response = client.recv(4096)

print response 

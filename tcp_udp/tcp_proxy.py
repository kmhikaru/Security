  # -*- coding: utf-8 -*-

import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Fialed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions"
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #print connection data from local host
        print "[==>] Received incoming connection from %s:%d" % (addr[0], addr[1])

        # start thread to connect to remote host

        proxy_thread = threading.Thread(
            target = proxy_handler,
            args = (client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():

    if len(sys.argv[1:]) != 5:
        print "Usage: ./tcp_proxy.py [localhost] [localport] [remotehost] [remote port] [receive_first]"
        print "Example: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    #settings (local)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    #settings (remote)
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    #set up socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    print "hello"
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)

            client_socket.send(remote_buffer)

    while True:

        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print "[==>] Received %d bytes from localhost." % len(local_buffer)



            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print "[==>] Send to remote."

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print "[<==] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)

            print "[<==] Send to localhost."

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more data. Closing connections."

            break



def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7f else b'.' for x in s])
        result.append( b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))

    print b'\n'.join(result)

def receive_from(connection):

    buffer = ""

    #let timeout time 2s
    connection.settimeout(2)

    try:

        while True:

            data = connection.recv(4096)

            if not data:
                brak

            buffer += data

    except:
        pass

    return buffer


def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer


main()

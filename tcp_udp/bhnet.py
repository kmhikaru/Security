# -*- coding: utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess

#define global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
	print "BHP Net Tool"
	print 
	print "Usage: bhnet.py -t target_host -p port"
	print "-l --listen              - listen on [host]:[port] for"
	print "                           incoming connection"
	print "-e --execute=file_to_run - execute the given file upon"
	print "                           receiving a connection"
	print "-c --command             - initialize a command shell"
	print "-u --upload=destination  - upon receiving connection upload a"
	print "                           file and write to [destination]"
	print
	print 
	print "Examples: "
	print "bphnet.py -t 192.168.0.1 -p 5555 -l -c"
	print "bphnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe"
	print "bphnet.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\""
	print "echo 'ABCDEFGHI' | ./hnet.py -t 192.168.11.12 -p 135"
	sys.exit(0)

def main():

	print "this is main"
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]):
		usage()
	#read command options
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hle:t:p:cu:",
			["help", "listen", "execute=", "target=",
			"port=","command", "upload="])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--commandshell"):
			command = True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert False, "Unhandled Option"
	
	if not listen and len(target) and port > 0:
		print "put input into buffer. if you dont send data to standard input push ctrl+D"	
		#put input into buffer
		#if you dont send data to standard input,push ctrl + D
		buffer = sys.stdin.read()
		print "send buffer to client sender"
		print buffer
		print "===="
		#send data
		client_sender(buffer)

	#start listening
	if listen:
		server_loop()


def client_sender(buffer):
	
	print "this is client sender"	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "socket done l99"
	try:
		#connect to target host	
		client.connect((target, port))
		print "connect l103"
		if len(buffer):
			client.send(buffer)
			print"send buffer l106"

		while True:
			#receiving
			recv_len = 1
			response = ""
			print "recv l112"
			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				print recv_len
				response+= data
				print response
			print "i wanna print response"	
			print response,
		
			#receiving additional data
			buffer = raw_input("")
			buffer += "\n"
		
			#send data
			client.send(buffer)

	except:
		print "[*] Exception! Exiting."
		
		#close the connection
		client.close()

def server_loop():
	print "this is server_loop"
	global target
	
	# if ip address is not specified
	# all interface wait till it will be specified
	if not len(target):
		target = "0.0.0.0"
	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	server.bind((target, port))

	server.listen(5)

	while True:
		client_socket, addr = server.accept()
		#start thread which handle a new connection
		client_thread = threading.Thread(
			target = client_handler, args=(client_socket,))
		client_thread.start()



def run_command(command):
	print "this is run command"
	#delete a new line in a tail of string
	command = command.rstrip()

	# execute command and get output
	try:
		output = subprocess.check_output(
			command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command.\r\n"
	
	#send output to client
	return output

def client_handler(client_socket):
	print "this is client handler"
	global upload
	global execute
	global command
	
	print "this is client handler"
	#check upload destination
	if len(upload_destination):
		
		# read all data and write data into file
		file_buffer = ""
	
		# receive data till sending data is finished 
		while True:
			data = client_socket.recv(1024)
		
			if len(data) == 0:
				break
			else:
				file_buffer += data
		
		#write data to file
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			#notify success or not in writing
			client_socket.send(
				"Successfully saved file to %s\r\n" % upload_destination)
		except:
			client_socket.send(
				"Failed to save file to %s\r\n" % upload_destination)
		
	# check whether command execution is specified or not
	if len(execute):
		
		#execute command
		output = run_command(execute)
		
		client_socket.send(output)
	
	# if commandshell execution is specified
	if command:
		
		#show prompt
		prompt = "<BHP:#> "
		client_socket.send(prompt)
		print "socket sending done"
		while True:
		
			#till enter key is pushed
			cmd_buffer = ""
			hoge = 0
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
				print cmd_buffer
				print hoge
				hoge += 1

			print"not while"
			# get result of command execution
			response = run_command(cmd_buffer)
			response += prompt

			# send command execution
			client_socket.send(response)

main()

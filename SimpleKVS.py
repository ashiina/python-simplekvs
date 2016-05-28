import re
import os
import time
import socket
import threading

PORT = 8888

class SimpleKVS:
	RESPONSE_SUCCESS = 0
	RESPONSE_ERROR = 1
	RESPONSE_NULL = '\0'
	RESPONSE_NEWLINE = '\n'

	storage = {}

	def __init__(self, host, port):
		listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		listen_socket.bind((host, port))
		listen_socket.listen(5)

		print 'Starting SimpleKVS server' 
		while True:
			client_connection, client_address = listen_socket.accept()
			threading.Thread(target = self.handle_connection, args = (client_connection, client_address)).start()

		print 'Finished'

	def handle_connection(self, client_connection, client_address):
		while True:
			request = client_connection.recv(1024).strip()
			print 'Received> "%s"' % request

			if not request:
				print 'Closing connection'
				client_connection.close()
				break

			# getter
			m = re.match(r'GET (.*)', request, re.M|re.I)
			if m and m.group(1):
				if m.group(1) in self.storage:
					client_connection.sendall('%s%s' % 
						(self.storage[m.group(1)], SimpleKVS.RESPONSE_NEWLINE)
					)
				else:
					client_connection.sendall('%s%s' % 
						(SimpleKVS.RESPONSE_NULL, SimpleKVS.RESPONSE_NEWLINE)
					)
				continue

			# setter
			m = re.match(r'SET (.*) (.*)', request, re.M|re.I)
			if m and m.group(1) and m.group(2):
				self.storage[m.group(1)] = m.group(2)
				client_connection.sendall('%s%s' % 
					(SimpleKVS.RESPONSE_SUCCESS, SimpleKVS.RESPONSE_NEWLINE)
				)
			else: 
				client_connection.sendall('%s%s' % 
					(SimpleKVS.RESPONSE_ERROR, SimpleKVS.RESPONSE_NEWLINE)
				)
				continue

kvs = SimpleKVS('', PORT)


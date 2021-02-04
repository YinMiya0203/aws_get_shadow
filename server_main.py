# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:16:31 2020

@author: Administrator
"""
import socket
import re

from multiprocessing import Process
from response_body import response_txt
import Debug
class HTTPServer(object):
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def start(self):
		self.server_socket.listen(128)
		Debug.DEBUG.print_debug("start ")
		while(True):
			client_socket, client_address = self.server_socket.accept()
			handle_client_process = Process(target=self.handle_client, args=(client_socket,))
			print("[%s, %s]connect" % client_address)
			handle_client_process.start()
			client_socket.close()

	def handle_client(self, client_socket):
		request_data = client_socket.recv(1024)
		print("request data:", request_data)
		request_lines = request_data.splitlines()
		if(len(request_lines)>1):
			request_start_line = request_lines[0]
			file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
			if "/" == file_name:
				host = request_lines[1].decode("utf-8").split(':')[1].strip()
				Debug.DEBUG.print_debug(host)
				response = response_txt(host=host)
				client_socket.send(response.get_index())
			elif "word=" in file_name:
				#key_word = re.match(r"\w+=+(/[^ ]*) ",file_name).group(0)
				host = request_lines[1].decode("utf-8").split(':')[1].strip()
				key_word,server,tz = file_name.split('=')[1].split('/')
				print("key_word: %s"% key_word)
				if server is None:
					s = response_txt.defdevelopment
					server = s.lower()
				if tz is None:
					tz = "+0800"
				server = server.strip()
				Debug.DEBUG.print_debug(host)
				response = response_txt(key_word,server.lower(),tz,host=host)
				client_socket.send(response.get_response())
			else:
				response = response_txt()
				client_socket.send(response.get_fail())
		# 关闭客户端连接
		client_socket.close()

	def bind(self, port):
		self.server_socket.bind(("", port))
def main():
	http_server = HTTPServer()
	http_server.bind(8000)
	http_server.start()

if __name__ == "__main__":
	main()

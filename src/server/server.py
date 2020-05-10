import socket
import ssl
import datetime
import os.path
import queue
import select
from server_cfg import ServerCFGUtility
from server_strings import *
from client_thread import ClientThread
from threading import Thread
import time
from server_utilities import *


class Server:
    def __init__(self):
        self.context = None
        self.client_list = None
        self.initialilze_server()
        self.inputs = []
        self.outputs = []
        self.message_queues = {}

    def initialilze_server(self):
        print(f"[Server] Initializing Server...")
        cfg_utility = ServerCFGUtility(os.path.dirname(os.path.abspath(__file__))+"/../configs/server_config.ini")
        server_cert = str(cfg_utility.get_value(key=SERVER_CERT_PATH, section=SERVER_FILES))
        server_pkey = str(cfg_utility.get_value(key=SERVER_PKEY_PATH, section=SERVER_FILES))
        ssl_ready = self.initialize_ssl_context(server_cert_path=server_cert, server_key_path=server_pkey)
        if not ssl_ready:
            print("[Server] There was an error establishing the SSL certification/key")
            return
        server_ip = str(cfg_utility.get_value(key=SERVER_IP, section=SERVER_SETTINGS))
        server_port = int(cfg_utility.get_value(key=SERVER_PORT, section=SERVER_SETTINGS))
        server_size = int(cfg_utility.get_value(key=SERVER_SIZE, section=SERVER_SETTINGS))
        server_tick_rate = float(cfg_utility.get_value(key=SERVER_TICK_RATE, section=SERVER_SETTINGS))
        bind_socket = self.initialize_bind_socket(server_ip, server_port)
        if not bind_socket:
            print(f"[Server] There was an error binding the socket to {server_ip}:{server_port}")
            return
        # Listen for connections with up to 'X' amount of connections
        bind_socket.listen(server_size)
        # Initialize a client list
        self.client_list = []
        print(f"[Server] Secure Server Online: {server_ip}:{server_port} - {datetime.datetime.now()}")
        self.run(bind_socket)

    def initialize_ssl_context(self, server_cert_path: str, server_key_path: str):
        # Setup context for client authentication
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        print(f"[Server] Setting up server certificates...")
        # Load server cert + server private key generated from openssl
        self.context.load_cert_chain(certfile=server_cert_path, keyfile=server_key_path)
        if self.context:
            return True
        return False

    def initialize_bind_socket(self, server_ip: str, server_port: int):
        # Create an IPv4 TCP Socket
        bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bind_socket.setblocking(0)
        # Bind socket to IP:Port
        bind_socket.bind((server_ip, server_port))
        self.inputs = [bind_socket]
        self.outputs = []
        self.message_queues = {}
        self.header_size = 8
        print(f"[Server] Setting up server on: {server_ip}:{server_port}")
        return bind_socket

    def close_socket(self, sock, sock_err=None):
        if sock_err:
            print(f"Client has unexpectedly disconnected: {sock.getpeername()}")
        else:
            print(f"Client has disconnected: {sock.getpeername()}")
        if sock in self.outputs:
            self.outputs.remove(sock)
        self.inputs.remove(sock)
        sock.close()
        del self.message_queues[sock]

    def handle_message_data(self, message, sock):
        if message == 'Hello!':
            self.message_queues[sock].put(prepare_message('!quit'))

    def send_message(self, sock, message):
        sock.send(bytes(message, 'utf-8'))
        if sock in self.outputs:
            self.outputs.remove(sock)
        self.inputs.remove(sock)

    def run(self, bind_socket):
        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            # Accept an incoming socket connection
            for sock in readable:
                # Check if the updated connection is a new socket.
                if sock is bind_socket:
                    insecure_socket, client_address = bind_socket.accept()
                    # Wrap the incoming socket into an SSL socket.
                    client_socket = self.context.wrap_socket(insecure_socket, server_side=True)
                    client_socket.setblocking(0)
                    self.inputs.append(client_socket)
                    self.message_queues[client_socket] = queue.Queue()
                # Handle data from clients.
                else:
                    try:
                        # Get header from 10 bytes (2 are formatting)
                        header = get_msg_header(sock)
                    except socket.error:
                        self.close_socket(sock, socket.error)
                        continue
                    message = get_message(header, sock)
                    if not message:
                        continue
                    print(f"[Client:{sock.getpeername()}]: {message}")
                    self.handle_message_data(message, sock)

            for sock in writable:
                try:
                    next_msg = self.message_queues[sock].get_nowait()
                except queue.Empty:
                    print(f"Output queue for {sock.getpeername()} is empty")
                    self.outputs.remove(sock)
                else:
                    print(f"Sending {next_msg} to {sock.getpeername()}")
                    self.send_message(sock, next_msg)

            for s in exceptional:
                print(f"Handling exceptional condition for {s.getpeername()}")
                self.close_socket(s)



if __name__ == "__main__":
    server = Server()

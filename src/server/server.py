import socket
import ssl
import datetime
import os.path
import queue
import select
import random

from server_cfg import ServerCFGUtility
import server_callbacks
import server_commands
from server_client import Client
from server_cfg_strings import SERVER_SETTINGS, SERVER_IP, SERVER_PORT, SERVER_TICK_RATE, SERVER_SIZE, SERVER_FILES, SERVER_CERT_PATH, SERVER_PKEY_PATH
from server_strings import *
from threading import Thread
import time
from server_utilities import prepare_message, get_message, get_msg_header


class Server:
    def __init__(self, name='Server'):
        self._name = name

        self.header_size = 8
        self.context = None

        self.inputs = []
        self.outputs = []
        self.clients = {}
        self.message_queues = {}

        self.commands = server_commands.ServerCommands()
        self.callbacks = server_callbacks.ServerCallbacks()
        self.serv_thread = None
        self.exit_flag = False
        self.bind_socket = self.setup_server()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def start_server(self):
        if self.bind_socket:
            self.serv_thread = Thread(target=self.run, args=(self.bind_socket,))
            self.serv_thread.start()
            self.callbacks.callback('on_server_start')

    def shutdown_server(self):
        self.exit_flag = True
        self.serv_thread.join()

    def setup_server(self):
        print(f"[{self.name}] Setting Up Server...")
        cfg_utility = ServerCFGUtility(os.path.dirname(os.path.abspath(__file__))+"/../configs/server_config.ini")
        server_cert = str(cfg_utility.get_value(key=SERVER_CERT_PATH, section=SERVER_FILES))
        server_pkey = str(cfg_utility.get_value(key=SERVER_PKEY_PATH, section=SERVER_FILES))
        ssl_ready = self.initialize_ssl_context(server_cert_path=server_cert, server_key_path=server_pkey)
        if not ssl_ready:
            print("[{self.name}] There was an error establishing the SSL certification/key")
            return None
        server_ip = str(cfg_utility.get_value(key=SERVER_IP, section=SERVER_SETTINGS))
        server_port = int(cfg_utility.get_value(key=SERVER_PORT, section=SERVER_SETTINGS))
        server_size = int(cfg_utility.get_value(key=SERVER_SIZE, section=SERVER_SETTINGS))
        self.server_tick_rate = float(cfg_utility.get_value(key=SERVER_TICK_RATE, section=SERVER_SETTINGS))
        bind_socket = self.initialize_bind_socket(server_ip, server_port)
        if not bind_socket:
            print(f"[{self.name}] There was an error binding the socket to {server_ip}:{server_port}")
            return None
        # Listen for connections with up to 'X' amount of connections
        bind_socket.listen(server_size)
        print(f"[{self.name}] Secure Server Established: {server_ip}:{server_port}")
        self.callbacks.callback('on_server_start')
        return bind_socket

    def initialize_ssl_context(self, server_cert_path: str, server_key_path: str):
        # Setup context for client authentication
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        print(f"[{self.name}] Setting up server certificates...")
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
        print(f"[{self.name}] Setting up server on: {server_ip}:{server_port}")
        return bind_socket

    def close_socket(self, sock, sock_err=None):
        client = self.find_client_by_socket(sock)
        if sock_err:
            print(f"Client has unexpectedly disconnected: {client.name}({sock.getpeername()})")
        else:
            print(f"Client has disconnected: {client.name}({sock.getpeername()})")

        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock in self.inputs:
            self.inputs.remove(sock)
        self.clients.pop(client.socket)
        del self.message_queues[sock]
        sock.close()

    def find_client_by_socket(self, sock):
        for client in self.clients:
            if self.clients[client].socket == sock:
                return self.clients[client]
        return None

    def set_client(self, client):
        self.clients[client.socket] = client

    def handle_message_data(self, command, *params):
        if command in self.commands:
            self.callbacks.callback(self.commands[command], *params)

    def send_message(self, data, sock=None):
        if data[SERV_DATA_TYPE] == SERV_BROADCAST:
            for sock in self.message_queues:
                if data[SERV_DATA_CLIENT] is None:
                    data[SERV_DATA_CLIENT] = self.name
                self.message_queues[sock].put(prepare_message(data))
                if sock not in self.outputs:
                    self.outputs.append(sock)
        elif data[SERV_DATA_TYPE] == SERV_MESSAGE:
            if not sock:
                return
            if data[SERV_DATA_CLIENT] is None:
                data[SERV_DATA_CLIENT] = self.name
            self.message_queues[sock].put(prepare_message(data))
            if sock not in self.outputs:
                self.outputs.append(sock)

    def send_data(self, sock, data):
        sock.send(bytes(data, 'utf-8'))
        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock not in self.inputs:
            self.inputs.append(sock)

    def run(self, bind_socket):
        while self.inputs and self.exit_flag is False:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            # Accept an incoming socket connection
            for sock in readable:
                # Check if the updated connection is a new socket.
                if sock is bind_socket:
                    #if self.callbacks.callback('on_new_connection', sock) is False:
                    #    print("rejected new socket")
                    #    self.close_socket(sock)
                    #    continue
                    insecure_socket, client_address = bind_socket.accept()
                    # Wrap the incoming socket into an SSL socket.
                    client_socket = self.context.wrap_socket(insecure_socket, server_side=True)
                    client_socket.setblocking(0)

                    new_client_id = random.SystemRandom().getrandbits(16)
                    new_client = Client(socket=client_socket, name=f"Client#{new_client_id}")
                    print(f"[{self.name}] New client connected, generated client {new_client.name}")
                    self.clients[new_client.socket] = new_client

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
                    message_json = get_message(header, sock)
                    if not message_json:
                        continue
                    message = message_json[SERV_DATA_CONTENT]
                    print(f"[SentFromClient-{self.find_client_by_socket(sock).name}({sock.getpeername()})]: {message}")
                    message_split = message.split(' ', 1)
                    if len(message_split) != 2:
                        message_split.append(None)
                    self.handle_message_data(message_split[0], sock, message_split[1])
                    # self.outputs.append(sock)

            for sock in writable:
                try:
                    for i in range(self.message_queues[sock].qsize()):
                        try:
                            next_msg = self.message_queues[sock].get_nowait()
                        except queue.Empty:
                            print(f"Output queue for {self.find_client_by_socket(sock).name}({sock.getpeername()}) is empty")
                            self.outputs.remove(sock)
                        else:
                            print(f"Sending {next_msg} to {self.find_client_by_socket(sock).name}({sock.getpeername()})")
                            self.send_data(sock, next_msg)
                except KeyError:
                    if sock in self.inputs:
                        self.inputs.remove(sock)
                    if sock in self.outputs:
                        self.outputs.remove(sock)
                    continue

            for sock in exceptional:
                print(f"Handling exceptional condition for {self.find_client_by_socket(sock).name}({sock.getpeername()})")
                self.close_socket(sock)

            time.sleep(self.server_tick_rate)

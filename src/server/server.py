import socket
import ssl
import datetime
import os.path
import queue
import select
from base64 import b64encode
from os import urandom
import random

from server_cfg import ServerCFGUtility
from server_strings import SERVER_SETTINGS, SERVER_IP, SERVER_PORT, SERVER_TICK_RATE, SERVER_SIZE, SERVER_FILES, SERVER_CERT_PATH, SERVER_PKEY_PATH
from client_thread import ClientThread
from threading import Thread
import time
from server_utilities import prepare_message, get_message, get_msg_header

from src.game.player import Player


class Server:
    def __init__(self):
        self.header_size = 8
        self.context = None
        self.client_list = None

        self.inputs = []
        self.outputs = []
        self.players = []
        self.message_queues = {}

        self.initialilze_server()


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
        self.server_tick_rate = float(cfg_utility.get_value(key=SERVER_TICK_RATE, section=SERVER_SETTINGS))
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
        print(f"[Server] Setting up server on: {server_ip}:{server_port}")
        return bind_socket

    def close_socket(self, sock, sock_err=None):
        player = self.find_player_by_socket(sock)
        if sock_err:
            print(f"Client has unexpectedly disconnected: {player.name}({sock.getpeername()})")
        else:
            print(f"Client has disconnected: {player.name}({sock.getpeername()})")

        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock in self.inputs:
            self.inputs.remove(sock)
        if player in self.players:
            self.players.remove(player)
        del self.message_queues[sock]
        sock.close()

    def find_player_by_socket(self, sock):
        for player in self.players:
            if player.socket == sock:
                return player
        return None

    def handle_message_data(self, message, sock):
        message_split = message.split(' ', 1)
        if message_split[0] == '!connect':
            if len(message_split) != 2:
                return
            new_player = self.find_player_by_socket(sock)
            new_name = message_split[1].strip()
            if message_split[1].strip().lower() in [player.name.lower() for player in self.players]:
                print("A client tried to join with the same name as an existing client. "
                      "A randomly generated name has been given instead.")
                new_name = f'#{random.SystemRandom().getrandbits(16)}'
            new_player.name = new_name
            self.message_queues[sock].put(prepare_message(f'[Server] Hello {new_player.name}! - {datetime.datetime.now()}'))
            return True
        elif message == '!leave':
            # self.message_queues[sock].put(prepare_message(f'!quit'))
            self.broadcast_message(sock, f"Client has disconnected: {self.find_player_by_socket(sock).name}({sock.getpeername()})")
            self.close_socket(sock)
            return False
        elif message == '!draw_card':
            # test code
            from src.game.deck import Deck
            deck = Deck(infinite_deck=True)
            card = deck.draw()
            self.message_queues[sock].put(prepare_message(f'[Server] {str(card)}'))
            return True
        else:
            self.broadcast_message(sock, f'{self.find_player_by_socket(sock).name} said - {message}')
            return True

    def broadcast_message(self, origin_sock, message):
        for sock in self.message_queues:
            self.message_queues[sock].put(prepare_message(f'[Server] {message}'))
            if self.message_queues[sock] != origin_sock:
                self.outputs.append(sock)

    def send_message(self, sock, message):
        sock.send(bytes(message, 'utf-8'))
        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock not in self.inputs:
            self.inputs.append(sock)

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

                    new_player_id = random.SystemRandom().getrandbits(16)
                    new_player = Player(socket=client_socket, name=f"#{new_player_id}")
                    print(f"New client connected, generated player {new_player.name}")
                    self.players.append(new_player)

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
                    print(f"[Client:{self.find_player_by_socket(sock).name}({sock.getpeername()})]: {message}")
                    if not self.handle_message_data(message, sock):
                        continue
                    self.outputs.append(sock)

            for sock in writable:
                try:
                    for i in range(self.message_queues[sock].qsize()):
                        try:
                            next_msg = self.message_queues[sock].get_nowait()
                        except queue.Empty:
                            print(f"Output queue for {self.find_player_by_socket(sock).name}({sock.getpeername()}) is empty")
                            self.outputs.remove(sock)
                        else:
                            print(f"Sending {next_msg} to {self.find_player_by_socket(sock).name}({sock.getpeername()})")
                            self.send_message(sock, next_msg)
                except KeyError:
                    if sock in self.inputs:
                        self.inputs.remove(sock)
                    if sock in self.outputs:
                        self.outputs.remove(sock)
                    continue

            for sock in exceptional:
                print(f"Handling exceptional condition for {self.find_player_by_socket(sock).name}({sock.getpeername()})")
                self.close_socket(sock)

            time.sleep(self.server_tick_rate)


if __name__ == "__main__":
    server = Server()

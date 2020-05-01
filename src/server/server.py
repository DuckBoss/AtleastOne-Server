import socket
import ssl
import datetime
import os.path
import queue
from server_cfg import ServerCFGUtility
from server_strings import *
from client_thread import ClientThread


class Server:
    def __init__(self):
        self.context = None
        self.client_list = None
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
        self.run(bind_socket, server_tick_rate)

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
        # Bind socket to IP:Port
        bind_socket.bind((server_ip, server_port))
        print(f"[Server] Setting up server on: {server_ip}:{server_port}")
        return bind_socket

    def run(self, bind_socket, server_tick_rate: int):
        while True:
            # Accept an incoming socket connection
            insecure_socket, client_address = bind_socket.accept()
            # Wrap the incoming socket into an SSL socket.
            client_socket = self.context.wrap_socket(insecure_socket, server_side=True)

            print(f"[Server] Client Connected: {client_address[0]}")
            client_result = queue.Queue()
            client_thread = ClientThread(client_socket, client_address, server_tick_rate, result=client_result)
            client_thread.setName(f"{client_address[0]}:{client_address[1]}")
            client_thread.start()
            self.client_list.append(
                {"thread": client_thread, "socket": client_socket, "address": client_address}
            )

            print(f"Total Clients:{len(self.client_list)}")
            client_done = client_result.get()
            if client_done:
                for item in self.client_list:
                    if item["address"][0] == client_address[0] and item["address"][1] == client_address[1]:
                        client_socket.close()
                        client_thread.join()
                        self.client_list.remove(item)
                        print(f"[Server] Client Disconnected: [{client_address[0]}:{client_address[1]}]")
                        break
            print(f"Total Clients:{len(self.client_list)}")




if __name__ == "__main__":
    server = Server()

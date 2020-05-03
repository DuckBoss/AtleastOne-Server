import socket
from threading import Thread
import time
import datetime
from server_utilities import prepare_message


class ClientThread(Thread):
    def __init__(self, client_socket, client_address, server_tick_rate, result=None):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.server_tick_rate = server_tick_rate
        self.socket_error = None
        if result:
            self.result = result
        print(f"[Server - ClientThread] New connection added: {client_address}")
        return

    def run(self):
        print(f"[Server - ClientThread] Connection established from: {self.client_address[0]}:{self.client_address[1]}")

        # Welcome message to all new clients
        msg = prepare_message(f"Secure Server Connection Established!")
        self.client_socket.send(bytes(msg, "utf-8"))

        # Looped messages to connected clients
        while True:
            time.sleep(self.server_tick_rate)
            msg = prepare_message("blah blah")
            try:
                if msg and len(msg) >= 0:
                    self.client_socket.send(bytes(msg, "utf-8"))
            except socket.error:
                if self.result:
                    self.result.put(f"{self.client_address[0]}:{self.client_address[1]}")
                    print(f"[Server - ClientThread] Connection closing: {self.client_address[0]}:{self.client_address[1]}")
                break


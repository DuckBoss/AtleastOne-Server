import socket
import ssl
import time
import datetime
import os.path
from server_utilities import prepare_message, send_all_cards


SERVER_SIZE = 5
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
SERVER_TICK_RATE = 0.3

print(f"Initializing Server...")
# Setup context for client authentication
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# Load server cert + server private key generated from openssl
context.load_cert_chain(certfile=os.path.dirname(__file__)+'/../server/server.pem', keyfile=os.path.dirname(__file__)+'/../server/server.key')
print(f"Setting up certificates...")
# Create an IPv4 TCP Socket
bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to IP:Port
bind_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Setting up server on: {SERVER_IP}:{SERVER_PORT}")
# Listen for connections with up to 'X' amount of connections
bind_socket.listen(SERVER_SIZE)
print(f"Secure Server Online: {SERVER_IP} - {datetime.datetime.now()}")

client_list = []
while True:
    # Accept an incoming socket connection
    insecure_socket, address = bind_socket.accept()
    # Wrap the incoming socket into an SSL socket.
    client_socket = context.wrap_socket(insecure_socket, server_side=True)
    print(f"Secure Connection established from {address[0]}")
    client_list.append(
        {"socket": client_socket, "address": address}
    )
    print(f"Client Connected: {address[0]}")


    # Welcome message to all new clients
    msg = prepare_message(f"Secure Server Connection Established!")
    client_socket.send(bytes(msg, "utf-8"))

    # Looped messages to connected clients
    while True:
        time.sleep(SERVER_TICK_RATE)

        msg = send_all_cards()
        try:
            if len(msg) >= 0:
                client_socket.send(bytes(msg, "utf-8"))
        except socket.error:
            for x in client_list:
                if x['socket'] == client_socket:
                    client_list.remove(x)
                    print(f"Client Disconnected: {x['address'][0]}")
                    break
            break

    client_socket.close()

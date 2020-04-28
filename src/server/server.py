import socket
import time
import datetime
import os.path
from server_utilities import prepare_message


SERVER_SIZE = 5
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
SERVER_TICK_RATE = 0.3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))

# server queue - allows for this number of incoming connections at a time
server.listen(SERVER_SIZE)

print(f"Server Online: {SERVER_IP} - {datetime.datetime.now()}")

client_list = []
while True:
    client_socket, address = server.accept()
    client_list.append(
        {"socket": client_socket, "address": address}
    )

    print(f"Connection established from {address[0]} - {datetime.datetime.now()}")

    # Welcome message to all new clients
    msg = prepare_message(f"Server Connection Established!")
    client_socket.send(bytes(msg, "utf-8"))

    # Looped messages to connected clients
    while True:
        time.sleep(SERVER_TICK_RATE)
        with open(os.path.dirname(__file__)+'/../test_files/test-all-cards.json', 'r') as json_file:
            msg = prepare_message(f"{json_file.read()}")
            try:
                client_socket.send(bytes(msg, "utf-8"))
            except socket.error:
                for x in client_list:
                    if x['socket'] == client_socket:
                        client_list.remove(x)
                        print(f"Client Disconnected: {x['address'][0]} - {datetime.datetime.now()}")
                        break
                break

    client_socket.close()

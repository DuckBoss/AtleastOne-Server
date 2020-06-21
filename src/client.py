import socket
import ssl
import time
import threading
import json
from server.server_utilities import prepare_message
from server.server_strings import *
from server import server_data

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
PLAYER_NAME = input("Enter a display name: ")
while len(PLAYER_NAME) == 0:
    PLAYER_NAME = input("Enter a display name: ")
SERVER_NAME = 'N/A'
HEADER_SIZE = 8
CLIENT_TICK_RATE = 0.1

print("Client Initializing...")
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
print(f"Connecting to server: [{SERVER_IP}:{SERVER_PORT}]")
insecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = context.wrap_socket(insecure_socket, server_hostname=SERVER_IP)
ssl_socket.connect((SERVER_IP, SERVER_PORT))

print(f"Server Certificate:\n{ssl.DER_cert_to_PEM_cert(ssl_socket.getpeercert(True))}")
print(f"Connnection Established: [{SERVER_IP}:{SERVER_PORT}]")
print("------------------------------------------------------------------")
print("This client currently implements a command-system for testing purposes")
print("This will be overridden when the C# client is made.")
print("------------------------------------------------------------------")
print("You can type commands into the console to send them to the server.")
print("\nAvailable commands: ")
print("!say <message>: Broadcasts a chat message to all clients on the server.")
print("!draw: Draws a random card from an infinite deck.")
print("!cards: Lists the cards currently on hand.")
print("!clients: Lists all the clients on the server.")
print("!start: Starts a game session, currently it only creates a deck and distributes 7 cards to each client.")
print("!stop: Stops an active game session and clears the hands of all clients.")
print("------------------------------------------------------------------")


def disconnect_from_server(reason=None):
    global kill_threads
    kill_threads = True
    if ssl_socket:
        ssl_socket.close()
    print(f"Client disconnected from server: [{SERVER_IP}:{SERVER_PORT}]")
    if reason:
        print(f'Client disconnected due to the following: {reason}')


def inbound_server_data():
    # Loop incoming messages
    while not kill_threads:
        try:
            # Get header from 10 bytes (2 are formatting)
            raw_header = ssl_socket.recv(HEADER_SIZE + 2)
        except socket.error as e:
            # print(e)
            disconnect_from_server()
            continue
        if len(raw_header) <= 0:
            continue
        # Get message length from given header info
        msg_len = int(raw_header[1:HEADER_SIZE + 1].decode("utf-8"))
        # Get the message based on the number of bytes stated in the header
        raw_msg = ssl_socket.recv(msg_len)
        header = raw_header.decode('utf-8')
        message = json.loads(raw_msg.decode('utf-8'))
        if message[SERV_DATA_CONTENT] == "!quit":
            disconnect_from_server()
        elif message[SERV_DATA_CONTENT].split(' ', 1)[0] == "!setname":
            global PLAYER_NAME
            PLAYER_NAME = message[SERV_DATA_CONTENT].split(' ', 1)[1]
            print(f'[DEBUG] Player name set: {PLAYER_NAME}')
        elif message[SERV_DATA_CONTENT].split(' ', 1)[0] == "!setserver":
            global SERVER_NAME
            SERVER_NAME = message[SERV_DATA_CLIENT]
            print(f'[DEBUG] Server name set: {SERVER_NAME}')
        else:
            print(f"{header}[{message[SERV_DATA_CLIENT] if message[SERV_DATA_CLIENT] is not None else SERVER_NAME}{' -> Me' if message[SERV_DATA_TYPE] != SERV_BROADCAST else ''}]:{message[SERV_DATA_CONTENT]}")


def outbound_data_to_server():
    # Send connect message
    connect_data = server_data.Data(content_type=SERV_MESSAGE, content_data=f"!connect {PLAYER_NAME}", client=PLAYER_NAME)
    ssl_socket.send(bytes(prepare_message(connect_data), 'utf-8'))
    while not kill_threads:
        try:
            # Send data to the server.
            data_to_send = input()
            if len(data_to_send) != 0:
                data_to_send = server_data.Data(content_type=SERV_MESSAGE, content_data=data_to_send, client=PLAYER_NAME)
                ssl_socket.send(bytes(prepare_message(data_to_send), 'utf-8'))
        except socket.error as e:
            # print(e)
            disconnect_from_server()
            return
        time.sleep(CLIENT_TICK_RATE)


# Kill flags
kill_threads = False

# Start inbound data retrieval.
inbound_thread = threading.Thread(target=inbound_server_data)
inbound_thread.start()
# Start outbound data sending.
outbound_thread = threading.Thread(target=outbound_data_to_server)
outbound_thread.start()







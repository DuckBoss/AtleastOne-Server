import socket
import ssl
import time
import threading
from server.server_utilities import prepare_message

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
PLAYER_NAME = input("Enter a display name: ")
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


def disconnect_from_server():
    global kill_threads
    kill_threads = True
    if ssl_socket:
        ssl_socket.close()
    print(f"Client disconnected from server: [{SERVER_IP}:{SERVER_PORT}]")


def inbound_server_data():
    # Loop incoming messages
    while not kill_threads:
        try:
            # Get header from 10 bytes (2 are formatting)
            header = ssl_socket.recv(HEADER_SIZE + 2)
        except socket.error as e:
            # print(e)
            disconnect_from_server()
            continue
        if len(header) <= 0:
            continue
        # Get message length from given header info
        header_len = int(header[1:HEADER_SIZE + 1].decode("utf-8"))
        # Get the message based on the number of bytes stated in the header
        full_msg = ssl_socket.recv(header_len)
        print(f"{header.decode('utf-8')}{full_msg.decode('utf-8')}")
        if full_msg.decode("utf-8") == "!quit":
            disconnect_from_server()


def outbound_data_to_server():
    # Send hello message
    ssl_socket.send(bytes(prepare_message(f"!connect {PLAYER_NAME}"), 'utf-8'))
    while not kill_threads:
        try:
            to_send = input()
            ssl_socket.send(bytes(prepare_message(to_send), 'utf-8'))
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







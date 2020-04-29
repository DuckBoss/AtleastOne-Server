import socket
import ssl

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
HEADER_SIZE = 8

print("Client Initializing...")
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
print(f"Connecting to server: [{SERVER_IP}:{SERVER_PORT}]")
insecure_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = context.wrap_socket(insecure_socket, server_hostname=SERVER_IP)
ssl_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Server Certificate:\n{ssl.DER_cert_to_PEM_cert(ssl_socket.getpeercert(True))}")
print(f"Connnection Established: [{SERVER_IP}:{SERVER_PORT}]")

# Receive welcome message
msg = ssl_socket.recv(1024)
if len(msg) > 0:
    print(msg.decode("utf-8"))
# Loop incoming messages
while True:
    # Get header from 10 bytes (2 are formatting)
    header = ssl_socket.recv(HEADER_SIZE+2)
    if len(msg) <= 0:
        continue
    # Get message length from given header info
    header_len = int(header[1:HEADER_SIZE+1].decode("utf-8"))
    print(header_len)
    # Get the message based on the number of bytes stated in the header
    full_msg = ssl_socket.recv(header_len)
    print(full_msg.decode("utf-8"))

print(f"Client disconnected from server: [{SERVER_IP}:{SERVER_PORT}]")


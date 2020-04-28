import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
HEADER_SIZE = 8

print("Client Initializing...")
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Connecting to server: [{SERVER_IP}:{SERVER_PORT}]")
serv.connect((SERVER_IP, SERVER_PORT))
print(f"Connnection Established: [{SERVER_IP}:{SERVER_PORT}]")

# Receive welcome message
msg = serv.recv(1024)
if len(msg) <= 0:
    print(msg.decode("utf-8"))
# Loop incoming messages
while True:
    # Get header from 10 bytes (2 are formatting)
    header = serv.recv(HEADER_SIZE+2)
    if len(msg) <= 0:
        continue
    # Get message length from given header info
    header_len = int(header[1:HEADER_SIZE+1].decode("utf-8"))
    print(header_len)
    # Get the message based on the number of bytes stated in the header
    full_msg = serv.recv(header_len)
    print(full_msg.decode("utf-8"))

print(f"Client disconnected from server: [{SERVER_IP}:{SERVER_PORT}]")


import json


HEADER_SIZE = 8


def prepend_msg_length_header(message):
    message = json.dumps(message)
    message = "[" + f"{len(message):<{HEADER_SIZE}}" + "]" + message
    return message


def prepare_message(data):
    data = prepend_msg_length_header(data)
    return data


def get_msg_header(socket):
    return socket.recv(HEADER_SIZE+2)


def get_message(header_msg, socket):
    if len(header_msg) <= 0:
        return None
    # Get message length from given header info
    header_len = int(header_msg[1:HEADER_SIZE + 1].decode("utf-8"))
    # Get the message based on the number of bytes stated in the header
    raw_data = socket.recv(header_len)
    msg_data = json.loads(bytes.decode(raw_data, 'utf-8'))
    return msg_data

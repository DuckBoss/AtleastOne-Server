HEADER_SIZE = 8


def prepend_msg_length_header(message):
    message = "[" + f"{len(message):<{HEADER_SIZE}}" + "]" + message
    return message


def prepare_message(message):
    message = prepend_msg_length_header(message)
    return message

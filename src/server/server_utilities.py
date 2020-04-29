HEADER_SIZE = 8


def prepend_msg_length_header(message):
    message = "[" + f"{len(message):<{HEADER_SIZE}}" + "]" + message
    return message


def prepare_message(message):
    message = prepend_msg_length_header(message)
    return message


def send_all_cards():
    import os
    with open(os.path.dirname(__file__) + '/../test_files/test-all-cards.json', 'r') as json_file:
        msg = prepare_message(f"{json_file.read()}")
        return msg

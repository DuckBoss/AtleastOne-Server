import random
import datetime
from server import Server
from src.server.server_utilities import prepare_message


def on_start():
    print("[Server] The server has started.")


def on_connect(socket, message):
    if message is None:
        return False
    new_player = server.find_player_by_socket(socket)
    if new_player.name_set_flag:
        return False
    new_name = message
    if message.lower() in [player.name.lower() for player in server.players]:
        print("[Server] A client tried to join with the same name as an existing client. "
              "A randomly generated name has been given instead.")
        new_name = f'User#{random.SystemRandom().getrandbits(16)}'
    new_player.name = new_name
    new_player.name_set_flag = True
    server.send_message(socket, f'[Server] Hello {new_player.name}!')
    return True


def on_message(*params):
    socket = params[0]
    message = params[1]
    server.broadcast_message(socket, f'[{server.find_player_by_socket(socket).name}]: {message}')
    print(f'[{server.find_player_by_socket(socket).name}]: {message}')
    return True


def on_disconnect(*params):
    socket = params[0]
    server.broadcast_message(socket, f"[Server] Client has disconnected: {server.find_player_by_socket(socket).name}({socket.getpeername()})")
    server.close_socket(socket)
    return False


def on_draw_card(*params):
    socket = params[0]
    from src.game.deck import Deck
    deck = Deck(infinite_deck=True)
    card = deck.draw()
    server.send_message(socket, f'[Server] {str(card)}')


server = Server()
server.callbacks.register_callback('on_client_connect', on_connect)
server.callbacks.register_callback('on_client_disconnect', on_disconnect)
server.callbacks.register_callback('on_server_start', on_start)
server.callbacks.register_callback('on_client_message', on_message)
server.callbacks.register_callback('on_draw_card', on_draw_card)
server.commands.register_command('!say', 'on_client_message')
server.commands.register_command('!draw', 'on_draw_card')
server.start_server()

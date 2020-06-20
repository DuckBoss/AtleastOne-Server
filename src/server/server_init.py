import random
import datetime
from server import Server
from src.game.logic import game
from src.game.player import Player
from src.server.server_utilities import prepare_message


def on_start():
    print("[Server] The server has started.")


def on_connect(*params):
    socket = params[0]
    message = params[1]
    if game_started:
        server.close_socket(sock=socket)
        return
    if message is None:
        return
    temp_client = server.find_client_by_socket(socket)
    new_client = Player(temp_client.socket, temp_client.name)
    if new_client.name_set_flag:
        return
    new_name = message
    if message.lower() in [server.clients[client].name.lower() for client in server.clients]:
        print("[Server] A client tried to join with the same name as an existing client. "
              "A randomly generated name has been given instead.")
    else:
        new_client.name = new_name
    new_client.name_set_flag = True
    server.set_client(new_client)
    server.send_message(socket, f'[Server] Hello {new_client.name}!')


def on_message(*params):
    socket = params[0]
    message = params[1]
    server.broadcast_message(f'[{server.find_client_by_socket(socket).name}]: {message}')
    print(f'[{server.find_client_by_socket(socket).name}]: {message}')


def on_disconnect(*params):
    global game_started
    socket = params[0]
    server.broadcast_message(f"[Server] Client has disconnected: {server.find_client_by_socket(socket).name}({socket.getpeername()})")
    if game_started:
        game.end_flag = True
        server.broadcast_message(f'[Server] The game was closed as {server.find_client_by_socket(socket).name} disconnected.')
    server.close_socket(socket)
    game_started = False


def on_get_clients(*params):
    socket = params[0]
    all_clients = [server.clients[client].name for client in server.clients]
    server.send_message(socket, f"[Server] All Clients: {', '.join(all_clients)}")


def on_draw_card(*params):
    socket = params[0]
    from src.game.deck import Deck
    deck = Deck(infinite_deck=True)
    card = deck.draw()
    server.send_message(socket, f'[Server] {str(card)}')


def on_view_cards(*params):
    socket = params[0]
    client = server.find_client_by_socket(sock=socket)
    if client:
        if client.hand_size() == 0:
            server.send_message(socket, f'[Server] {client.name} has no cards on hand.')
            server.outputs.append(socket)
            return
        for card in client.hand.deck:
            server.send_message(socket, f'[Server] {str(card)}')


def on_game_start(*params):
    global game_started
    if not game_started:
        game_started = True
        game.game_loop(server=server)


game_started = False
server = Server()
server.callbacks.register_callback('on_client_connect', on_connect)
server.callbacks.register_callback('on_client_disconnect', on_disconnect)
server.callbacks.register_callback('on_server_start', on_start)
server.callbacks.register_callback('on_client_message', on_message)
server.callbacks.register_callback('on_draw_card', on_draw_card)
server.callbacks.register_callback('on_get_clients', on_get_clients)
server.callbacks.register_callback('on_game_start', on_game_start)
server.callbacks.register_callback('on_view_cards', on_view_cards)
server.commands.register_command('!say', 'on_client_message')
server.commands.register_command('!draw', 'on_draw_card')
server.commands.register_command('!cards', 'on_view_cards')
server.commands.register_command('!clients', 'on_get_clients')
server.commands.register_command('!start', 'on_game_start')
server.start_server()

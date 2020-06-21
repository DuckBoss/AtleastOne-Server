import random
import datetime
from server import Server
from src.game.logic import game
from src.game.player import Player
from src.server import server_data
from src.server.server_strings import *
from src.server.server_utilities import prepare_message


def on_start():
    print(f"[{server.name}] The server has started.")


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
        print(f"[{server.name}] A client tried to join with the same name as an existing client. "
              "A randomly generated name has been given instead.")
    else:
        new_client.name = new_name
    new_client.name_set_flag = True
    server.set_client(new_client)
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'!setname {new_client.name}'), sock=socket)
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'!setserver'), sock=socket)
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'Hello {new_client.name}!'), sock=socket)
    server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'{new_client.name} joined the server.'))


def on_message(*params):
    socket = params[0]
    message = params[1].strip()
    if len(message) != 0:
        server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'{message}', client=server.find_client_by_socket(socket).name))
        print(f'[{server.find_client_by_socket(socket).name}]: {message}')


def on_disconnect(*params):
    global game_started
    socket = params[0]
    server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f"Client has disconnected: {server.find_client_by_socket(socket).name}({socket.getpeername()})"))
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data='!quit'), sock=socket)
    if game_started:
        game.end_flag = True
        server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'The game was closed as {server.find_client_by_socket(socket).name} disconnected.'))
    game_started = False
    server.close_socket(socket)


def on_get_clients(*params):
    socket = params[0]
    all_clients = [server.clients[client].name for client in server.clients]
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f"All Clients ({len(server.clients)}) -  {', '.join(all_clients)}"), sock=socket)


def on_draw_card(*params):
    socket = params[0]
    from src.game.deck import Deck
    deck = Deck(infinite_deck=True)
    card = deck.draw()
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'{str(card)}'), sock=socket)


def on_view_cards(*params):
    socket = params[0]
    client = server.find_client_by_socket(sock=socket)
    if client:
        if client.hand_size() == 0:
            server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'{client.name} has no cards on hand.'), sock=socket)
            # server.outputs.append(socket)
            return
        for card in client.hand.deck:
            server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'{str(card)}'), sock=socket)


def on_game_start(*params):
    socket = params[0]
    client = server.find_client_by_socket(socket)
    global game_started
    if not game_started:
        game_started = True
        server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'The game has been started by {client.name}'), sock=socket)
        game.game_loop(server=server)


def on_game_stop(*params):
    socket = params[0]
    client = server.find_client_by_socket(socket)
    global game_started
    if game_started:
        game_started = False
        server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'The game has been closed by {client.name}'))
        game.clear_game(server=server)


game_started = False
server = Server(name='UnoServer')
server.callbacks.register_callback('on_client_connect', on_connect)
server.callbacks.register_callback('on_client_disconnect', on_disconnect)
server.callbacks.register_callback('on_server_start', on_start)
server.callbacks.register_callback('on_client_message', on_message)
server.callbacks.register_callback('on_draw_card', on_draw_card)
server.callbacks.register_callback('on_get_clients', on_get_clients)
server.callbacks.register_callback('on_game_start', on_game_start)
server.callbacks.register_callback('on_game_stop', on_game_stop)
server.callbacks.register_callback('on_view_cards', on_view_cards)
server.commands.register_command('!say', 'on_client_message')
server.commands.register_command('!draw', 'on_draw_card')
server.commands.register_command('!cards', 'on_view_cards')
server.commands.register_command('!clients', 'on_get_clients')
server.commands.register_command('!start', 'on_game_start')
server.commands.register_command('!stop', 'on_game_stop')
server.start_server()

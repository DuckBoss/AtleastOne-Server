from src.game.deck import Deck
from src.server.server_utilities import prepare_message, get_message, get_msg_header
import time


end_flag = False


def clear_game(server):
    global end_flag
    end_flag = False
    for client in server.clients:
        server.clients[client].hand = Deck()


def game_loop(server):
    game_deck = Deck(infinite_deck=True)
    server.broadcast_message(f'[Server] THE GAME HAS BEGUN!')
    for client in server.clients:
        while server.clients[client].hand_size() < 7:
            card = game_deck.draw()
            server.clients[client].add_to_hand(card)
            server.send_message(server.clients[client].socket, f'[Server] Given {server.clients[client].name}: {card.get_json()}')
            # server.send_data(player.socket, )

    while not end_flag:
        time.sleep(1)
    clear_game(server)

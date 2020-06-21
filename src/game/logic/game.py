from src.game.deck import Deck
from src.server import server_data
from src.server.server_strings import *
import time

end_flag = False


def clear_game(server):
    global end_flag
    end_flag = False
    for client in server.clients:
        server.clients[client].hand = Deck()


def game_loop(server):
    game_deck = Deck()
    game_deck.generate_default_deck(num_of_players=len(server.clients), card_definitions_file='../definitions/cards.json')
    print(f"Deck Size: {game_deck.size}")
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'THE GAME HAS STARTED!', client=server.name))
    for client in server.clients:
        while server.clients[client].hand_size() < 7:
            card = game_deck.draw()
            server.clients[client].add_to_hand(card)
            server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'Given {server.clients[client].name}: {card.get_json()}', client=server.name), sock=server.clients[client].socket)
            print(f'Cards left in deck: {game_deck.size}')

    while not end_flag:
        time.sleep(1)
    clear_game(server)

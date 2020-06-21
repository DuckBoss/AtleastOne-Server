from src.game.deck import Deck
from src.server import server_data
from src.server.server_strings import *
import time
import random

end_flag = False


def clear_game(server):
    global end_flag
    end_flag = False
    for client in server.clients:
        server.clients[client].hand = Deck()


def game_loop(server):
    game_deck = Deck()
    discard_pile = Deck()
    game_deck.generate_default_deck(num_of_players=len(server.clients), card_definitions_file='../definitions/cards.json')
    print(f"Deck Size: {game_deck.size}")
    server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'THE GAME HAS STARTED!', client=server.name))
    for client in server.clients:
        while server.clients[client].hand_size() < 7:
            card = game_deck.draw()
            server.clients[client].add_to_hand(card)
            server.send_message(server_data.Data(content_type=SERV_MESSAGE, content_data=f'Given {server.clients[client].name}: {card.get_json()}', client=server.name), sock=server.clients[client].socket)
            print(f'Cards left in deck: {game_deck.size}')

    # Draw first card
    discard_pile.add_to_top(game_deck.draw())
    print(f"Chosen Card - {discard_pile.get_top_card()}")
    server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'Discard Pile: Top Card - {discard_pile.get_top_card()}'))

    # Get first player
    current_player = random.choice(list(server.clients.values()))
    print(f"First Player - {current_player.name}")
    server.send_message(server_data.Data(content_type=SERV_BROADCAST, content_data=f'The first player is {current_player.name}'))

    while not end_flag:
        time.sleep(1)
    clear_game(server)

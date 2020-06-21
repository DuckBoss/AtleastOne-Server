from src.game.card import Card
from src.game.deck import Deck
from src.server import server_data
from src.server.server_strings import *
import time
import random
import json

end_flag = False
current_player = None
game_deck = None
discard_pile = None
registered_cards = []


def clear_game(server):
    global end_flag
    end_flag = False
    for client in server.clients:
        server.clients[client].hand = Deck()


def end_turn(server, clockwise=True):
    global current_player
    all_sockets = list(server.clients)
    for i, socket in enumerate(all_sockets):
        if socket == current_player.socket:
            if clockwise is True:
                if i+1 >= len(all_sockets):
                    current_player = server.find_client_by_socket(all_sockets[0])
                else:
                    current_player = server.find_client_by_socket(all_sockets[i+1])
            else:
                current_player = server.find_client_by_socket(all_sockets[i-1])
            server.send_message(server_data.Data(content_type=SERV_BROADCAST,
                                                 content_data=f'Discard Pile: Top Card - {discard_pile.get_top_card()}'))
            server.send_message(server_data.Data(content_type=SERV_BROADCAST,
                                                 content_data=f'It is {current_player.name}\'s turn.'))
            return


def register_cards():
    global registered_cards
    with open('../definitions/cards.json', 'r') as card_defs:
        data = json.load(card_defs)
        # Retrieve all cards
        for card_color in data['cards']['colors']:
            for card_value in data['cards']['colors'][card_color]['values']:
                registered_cards.append(
                    Card(card_color=card_color, card_value=card_value,
                         card_hex=data['cards']['colors'][card_color]['hex'])
                )
    print("Registered all cards.")


def game_loop(server):
    global current_player, game_deck, discard_pile, registered_cards

    register_cards()
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

from src.game.deck import Deck
from src.server import server_data
import time

end_flag = False


def clear_game(server):
    global end_flag
    end_flag = False
    for client in server.clients:
        server.clients[client].hand = Deck()


def game_loop(server):
    game_deck = Deck()
    game_deck.generate_default_deck(card_definitions_file='../definitions/cards.json')
    server.broadcast_message(server_data.Data(content_type='message', content_data=f'THE GAME HAS BEGUN!', client=server.name))
    for client in server.clients:
        while server.clients[client].hand_size() < 7:
            card = game_deck.draw()
            server.clients[client].add_to_hand(card)
            server.send_message(server.clients[client].socket, server_data.Data(content_type='message', content_data=f'Given {server.clients[client].name}: {card.get_json()}', client=server.name))
            print(f'Cards left in deck: {game_deck.size}')

    while not end_flag:
        time.sleep(1)
    clear_game(server)

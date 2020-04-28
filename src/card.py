import json


class Card:
    def __init__(self, card_type: str, card_color: str, card_number: int = -1, card_hex: str = ''):
        self.CardType = card_type
        self.CardColor = card_color
        self.CardNumber = card_number
        self.CardHex = card_hex

    def get_json(self):
        return {
            'type': self.CardType,
            'color': self.CardColor,
            'number': self.CardNumber,
            'hex': self.CardHex
        }

    def get_json_dump(self):
        return json.dumps(
            {
                'type': self.CardType,
                'color': self.CardColor,
                'number': self.CardNumber,
                'hex': self.CardHex
            }
        )

    def __str__(self):
        return f"{self.CardType}-{self.CardColor}-{self.CardNumber}"

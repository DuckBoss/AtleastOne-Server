from zlib import adler32


class Card:
    def __init__(self, card_color: str, card_value: str = "-1", card_hex: str = ''):
        self.value = card_value
        self.color = card_color
        self.hex = card_hex
        self.id = self.generate_id()

    def generate_id(self):
        return adler32(bytes(f"{self.color}{self.value}{self.hex}", 'utf-8'))

    def get_json(self):
        return {
            'id': self.id,
            'color': self.color,
            'value': self.value,
            'hex': self.hex
        }

    def get_json_dump(self):
        from json import dumps
        return dumps(self.get_json())

    def __str__(self):
        return f"Card (ID - {self.id}, Value - {self.value}, Color = {self.color}, Hex - {self.hex})"

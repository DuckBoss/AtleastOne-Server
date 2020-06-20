class Client:
    def __init__(self, socket, name):
        self._socket = socket
        self._name = name
        self.name_set_flag = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def socket(self):
        return self._socket
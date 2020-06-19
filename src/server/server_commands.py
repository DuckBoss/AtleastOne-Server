class ServerCommands(dict):
    def __init__(self):
        super().__init__()
        self.update({
            '!connect': 'on_client_connect',
            '!disconnect': 'on_client_disconnect'
        })

    def register_command(self, command, callback_name):
        self[command] = callback_name

    def remove_command(self, command):
        try:
            del self[command]
            return True
        except KeyError:
            return False

    def get_command(self, get_command):
        try:
            self[get_command]
        except KeyError:
            return None

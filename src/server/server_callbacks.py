from threading import Thread


class ServerCallbacks(dict):
    def __init__(self):
        super().__init__()
        self.update({
            'on_client_connect': None,
            'on_client_disconnect': None,
            'on_server_start': None,
        })

    def register_callback(self, callback, dest):
        self[callback] = dest

    def remove_callback(self, callback):
        try:
            del self[callback]
            return True
        except KeyError:
            return False

    def get_callback(self, callback):
        try:
            self[callback]
        except KeyError:
            return None

    def callback(self, callback, *params):
        if self[callback]:
            thr = Thread(target=self[callback], args=params)
            thr.start()

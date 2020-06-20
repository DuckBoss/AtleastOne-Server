import json


class Data(dict):
    def __init__(self, content_type, content_data, client=None):
        super().__init__()
        self.content_type = content_type
        self.content_data = content_data
        self.client = client
        self.update({
            f'data_type': self.content_type,
            f'data_content': self.content_data,
            f'client': self.client
        })

    def update_type(self, content_type):
        self['data_type'] = content_type

    def update_content(self, content_data):
        self['data_content'] = content_data

    def update_client(self, client):
        self['client'] = client

    def as_json(self):
        return json.dumps(self)

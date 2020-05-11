import configparser


class ServerCFGUtility:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_value(self, key, section=None):
        if section:
            return self.config[section][key]
        return self.config[key]

    def get_full_config(self):
        return self.config

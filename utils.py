import json


API_KEY = 'api_key'
SELENIUM_HUB = 'selenium_hub'
BROWSER = 'browser'


class LoadConfig:

    def __init__(self):
        with open('config.json') as f:
            self.data = json.load(f)

    def get_value(self, key):
        return self.data[key]

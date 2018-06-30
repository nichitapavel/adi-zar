import json
import xmltodict as xtoj

from requests.utils import urlunparse
from requests.api import get
from urllib.parse import urlencode, urlparse
from http import HTTPStatus


UNITS = 'metric'
API_KEY = 'c433ce2c47008f591668cbcf78df75db'
CITY = 'Zaragoza'
COUNTRY = 'ES'
CITY_NOT_FOUND_MESSAGE = 'city not found'
ROOT_URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_url(args_dict):
    url_parts = list(urlparse(ROOT_URL))
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)


class TestWeather:

    def test_get_correct_city(self):
        response = get(get_url({'q': f'{CITY},{COUNTRY}', 'appid': f'{API_KEY}'}))
        res_json = json.loads(response.text)
        assert CITY == res_json['name']

    def test_unknown_city_no_response(self):
        unknown = 'UNKNOWN'
        response = get(get_url({'q': f'{unknown},{COUNTRY}', 'appid': f'{API_KEY}'}))
        res_json = json.loads(response.text)

        assert HTTPStatus.NOT_FOUND == response.status_code
        assert CITY_NOT_FOUND_MESSAGE == res_json['message']

    def test_get_units_imperial(self):
        response = get(get_url({'q': f'{CITY},{COUNTRY}', 'appid': f'{API_KEY}',
                                'mode': 'xml', 'units': 'imperial'}))
        res_json = json.loads(json.dumps(xtoj.parse(response.text, attr_prefix='')))

        assert res_json['current']['temperature']['unit'] == 'fahrenheit'

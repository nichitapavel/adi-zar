import json
import xmltodict as xtoj

from requests.utils import urlunparse
from requests.api import get
from urllib.parse import urlencode, urlparse
from http import HTTPStatus
from utils import LoadConfig, API_KEY


UNITS = 'metric'
CITY = 'Zaragoza'
COUNTRY = 'ES'
CITY_NOT_FOUND_MESSAGE = 'city not found'
ROOT_URL = 'https://api.openweathermap.org/data/2.5/weather'


def get_url(args_dict):
    """
    util method to build the api url, needs improvement
    :param args_dict: A dictionary with query of a url, format is key: value, that translates into 'http...?key=value'
    :return:
    """
    url_parts = list(urlparse(ROOT_URL))
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)


class TestWeather:

    def setup_method(self):
        self.api_key = LoadConfig().get_value(API_KEY)

    def test_get_correct_city(self):
        """
        Checks weather for a city and checks that response is describing the city asked and not another one.
        :return:
        """
        response = get(get_url({'q': f'{CITY},{COUNTRY}', 'appid': f'{self.api_key}'}))
        res_json = json.loads(response.text)
        assert CITY == res_json['name']

    def test_unknown_city_no_response(self):
        """
        Checks weather for a city named 'Unknown' in Spain, city does not exist it should response with
        a 'not found' message
        :return:
        """
        unknown = 'UNKNOWN'
        response = get(get_url({'q': f'{unknown},{COUNTRY}', 'appid': f'{self.api_key}'}))
        res_json = json.loads(response.text)

        assert HTTPStatus.NOT_FOUND == response.status_code
        assert CITY_NOT_FOUND_MESSAGE == res_json['message']

    def test_get_units_imperial(self):
        """
        Checks that if we ask a different measurement metric we get what we asked for.
        :return:
        """
        response = get(get_url({'q': f'{CITY},{COUNTRY}', 'appid': f'{self.api_key}',
                                'mode': 'xml', 'units': 'imperial'}))
        res_json = json.loads(json.dumps(xtoj.parse(response.text, attr_prefix='')))

        assert res_json['current']['temperature']['unit'] == 'fahrenheit'

    def test_has_weather(self):
        """
        Checks that if we ask a different measurement metric we get what we asked for.
        :return:
        """
        response = get(get_url({'q': f'{CITY},{COUNTRY}', 'appid': f'{self.api_key}'}))
        res_json = json.loads(response.text)

        assert res_json['weather'][0]['description'] is not None

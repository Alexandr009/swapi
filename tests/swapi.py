import requests
import json
from pathlib import Path


class APIRequester():

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, sw_type=''):
        try:
            url = ''
            if not sw_type:
                url = self.base_url
            else:
                if not self.base_url.endswith('/') and not sw_type.startswith('/'):
                    url = f'{self.base_url}/{sw_type}'
                else:
                    url = f'{self.base_url}{sw_type}'

            respons = requests.get(url)
            if respons.status_code == 200:
                return respons
            else:
                return '<ошибка на сервере>'

        except requests.ConnectionError:
            print('Возникла ошибка при выполнении запроса')
            return 'сетевая ошибка'
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')
            return 'ошибка соединения'
        except requests.HTTPError:
            print('Возникла ошибка при выполнении запроса')
            return 'HTTP сервера'
        except requests.Timeout:
            print('Возникла ошибка при выполнении запроса')
            return 'тай маут ошибка'


class SWRequester(APIRequester):

    def get_sw_categories(self):
        response = self.get('/')
        dict_result = json.loads(response.text)
        for category, url in dict_result.items():
            print(f"Категория: {category}")
            print(f"URL: {url}\n")
        return dict_result.keys()

    def get_sw_info(self, sw_type):
        if not sw_type or not sw_type.strip():
            return "Ошибка: тип не может быть пустым"
        response = self.get(f'{sw_type}/')
        return response.text


def save_sw_data():
    path_name = 'data'
    Path(path_name).mkdir(exist_ok=True)
    objectSw = SWRequester('https://swapi.dev/api')
    categories = objectSw.get_sw_categories()
    for category in list(categories):
        with open(f'{path_name}/{category}.txt', 'w', encoding='utf-8') as file:
            text = objectSw.get_sw_info(category)
            file.write(text)
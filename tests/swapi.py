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
        if self.base_url.endswith('/'):
            url = self.base_url
        else:
            url = f'{self.base_url}/'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                dict_result = json.loads(response.text)
                print(dict_result)
                for category, url in dict_result.items():
                    print(f"Категория: {category}")
                    print(f"URL: {url}\n")
                return dict_result.keys()
            else:
                return f'<ошибка на сервере: {response.status_code}>'
        except requests.ConnectionError:
            return 'сетевая ошибка'
        except requests.RequestException:
            return 'ошибка соединения'
        except json.JSONDecodeError:
            return "Ошибка декодирования JSON"

    def get_sw_info(self, sw_type):
        if not sw_type or not sw_type.strip():
            return "Ошибка: тип не может быть пустым"

        if self.base_url.endswith('/') and sw_type.startswith('/'):
            url = f'{self.base_url}{sw_type[1:]}/'
        elif not self.base_url.endswith('/') and not sw_type.startswith('/'):
            url = f'{self.base_url}/{sw_type}/'
        else:
            url = f'{self.base_url}{sw_type}/'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return f'<ошибка на сервере: {response.status_code}>'
        except requests.ConnectionError:
            return 'сетевая ошибка'
        except requests.RequestException:
            return 'ошибка соединения'


def save_sw_data():
    Path("data").mkdir(exist_ok=True)
    objectSw = SWRequester('https://swapi.dev/api')
    categories = objectSw.get_sw_categories()
    for category in list(categories):
        with open(f'data/{category}.txt', 'w', encoding='utf-8') as file:
            text = objectSw.get_sw_info(category)
            file.write(text)

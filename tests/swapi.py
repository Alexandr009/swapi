import requests
import json

class APIRequester():
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, sw_type=''):
        try:
            respons = requests.get(f'{self.base_url}{sw_type}')
            if respons.status_code == 200:
                return respons # возвращать объект класса Response
            else:
                 return '<ошибка на сервере>'

        except requests.ConnectionError:
              return 'сетевая ошибка'
        except requests.RequestException:
              return 'ошибка соединения'
        except requests.HTTPError:
              return 'HTTP сервера'
        except requests.Timeout:
              return 'тай маут ошибка'

class SWRequester(APIRequester):
     
    def get_sw_categories(self):
        result = self.get()
        #for item in result.text:
        #    print(item)
        dict_result = json.loads(result.text)
        print(dict_result)
        for category, url in dict_result.items():
            print(f"Категория: {category}")
            print(f"URL: {url}\n")
            print(self.get_sw_info(category))

     
    def get_sw_info(self, sw_type):
        #respons = requests.get(f'{self.base_url}{sw_type}/')
        result = self.get(sw_type)
        return result.text
    
    def save_sw_data(self):
        pass

if __name__ == '__main__':
    objectSw = SWRequester('https://swapi.dev/api/')
    objectSw.get_sw_categories()
import requests
import json

class APIRequester():
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, sw_type=''):
        try:
            url = ''
            if not sw_type:
                url = self.base_url
            else:
                # Добавляем слеш между base_url и sw_type если нужно
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
        result = self.get()
        #for item in result.text:
        #    print(item)
        dict_result = json.loads(result.text)
        print(dict_result)
        for category, url in dict_result.items():
            print(f"Категория: {category}")
            print(f"URL: {url}\n")
            #print(self.get_sw_info(category))
            #print(self.get_sw_info(url))

     
    def get_sw_info(self, sw_type):
        #result = self.get(sw_type)
        #return result.text
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

    
    def save_sw_data(self):
        pass

if __name__ == '__main__':
    objectSw = SWRequester('https://swapi.dev/api/')
    objectSw.get_sw_categories()
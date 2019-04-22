#Библиотека для get/post запросов
import requests

class BotGoogle:

    #Определяем объект, задаём ему сайт с API, которому посылалать запросы
    def __init__(self, token):
        #Токен - адрес на API GoogleMaps Geocoding
        self.token = token

    #Возвращает нам название улицы, на которой находятся координаты
    def google_maps (self,coords):
        self.coords = coords
        self.api_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}".format(coords [0], coords [1], self.token)
        resp = requests.get (self.api_url)
        #Проверка правильности запроса
        if resp.json () ['status'] == 'OK':
            result_json = resp.json () ['results'] [0] ['address_components']
            #Поиск улиц
            if result_json [0] ['types'] == ['route']:
                name_street = result_json [0] ['long_name']
            elif result_json [1] ['types'] == ['route']:
                name_street = result_json [1] ['long_name']
            else:
                #Если в запрашиваемой точке нет улицы
                name_street = 'Unnamed Road'
        else:
            #Если в запрашиваемой точке нет улицы
            name_street = 'Unnamed Road'
        return name_street


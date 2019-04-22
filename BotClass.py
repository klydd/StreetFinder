#Библиотека для get/post запросов
import requests

class BotHandler:

    #Определение объект, задаём ему сайт с API, которому посылалать запросы
    def __init__(self, token):
        #Токен - адрес на API
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #Запрос /getUpdates на API Telegram
    def get_updates(self, offset = None, timeout = 5):
        method = 'getUpdates'
        #Параметры, которые задаются при запросе на API
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        #Получаем данные в формате json
        result_json = resp.json()['result']
        return result_json

    #Запрос /sendMessage на API Telegram (отправляем сообщение пользователю)
    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        resp = requests.post(self.api_url + method, params)
        return resp

    #Зацикливание получения обновлений
    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result [-1]
        else:
            last_update = None

        return last_update


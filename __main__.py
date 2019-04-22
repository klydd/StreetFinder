#Библиотека для регулярных выражений
#Библиотека для get/post запросов
#Основной бот
#Связь с API GoogleMaps
import re
import requests
from BotClass import BotHandler
from BotGoogler import BotGoogle

#Токен - адрес на API
token_telegram = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
#Лимит запросов на день от GoogleMaps Geocoding API- 2500
token_google_maps = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

bot = BotHandler (token_telegram)

#Функция, добавляющая название улиц на определённых координатах, в список
def append_coords (coordx, coordy, a, r, google_bot):
    a.append (google_bot.google_maps (coords = [coordx + r, coordy + r]))
    a.append (google_bot.google_maps (coords = [coordx + r, coordy - r]))
    a.append (google_bot.google_maps (coords = [coordx - r, coordy + r]))
    a.append (google_bot.google_maps (coords = [coordx - r, coordy - r]))
    a.append (google_bot.google_maps (coords = [coordx + r, coordy]))
    a.append (google_bot.google_maps (coords = [coordx - r, coordy]))
    a.append (google_bot.google_maps (coords = [coordx, coordy - r]))
    a.append (google_bot.google_maps (coords = [coordx,coordy + r]))

def main ():
    new_offset = None
    google_bot = BotGoogle(token_google_maps)
    
    while True:
        bot.get_updates (new_offset)

        last_update = bot.get_last_update ()
        
        if not last_update:
            continue

        #Получение нужных данных из обновлений
        last_update_id = last_update ['update_id']
        last_chat_text = last_update ['message'] ['text']
        last_chat_id = last_update ['message'] ['chat'] ['id']
        last_chat_name = last_update ['message'] ['chat'] ['first_name']

        #Регулярное выражение, которое ищет координаты и радиус
        coords = re.findall (r'[-]*\d+\.\d+', last_chat_text)

        #Запуск основного алгоритма
        if len (coords) == 3 or len (coords) == 2:

            #Высчитывание радиуса
            if len (coords) < 3:
                rad = (re.findall (r'\d+$', last_chat_text) [0])
            else:
                rad = (coords [2])
                del coords [2]

            if len (rad) > 3:
                bot.send_message (last_chat_id, 'Ошибка ввода радиуса')
                new_offset = last_update_id + 1
                continue
            
            rad = float (rad)
            
            #Необходимые переменные
            #n - радиус, переведённый в формат координат из рассчёта
            #10 m = 0.000200 coords
            a = []
            r = 0
            n = rad * 0.02
            coordx = float(coords [0])
            coordy = float(coords [1])

            bot.send_message (last_chat_id, 'Веду поиск')

            #Поиск улиц
            while r <= n:

                coordx_new = coordx + r
                coordy_new = coordy + r
                
                if (coordx_new == coordx):
                    a.append (google_bot.google_maps (coords = [coordx, coordy]))
                    r += 0.003
                    continue

                #На координаты (+, +)
                if coordx > 0 and coordy > 0:
                    if (coordx_new ** 2 + coordy_new ** 2) <= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)
 
                #На координаты (-, -)
                elif coordx < 0 and coordy < 0:
                    if (coordx_new ** 2 + coordy_new ** 2) >= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)

                #Координаты (+, -)
                elif coordx > 0 and coordy < 0:
                    if (coordx_new ** 2 + coordy_new ** 2) >= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)

                #Координаты (-, +)
                elif coordx < 0 and coordy > 0:
                    if (coordx_new ** 2 + coordy_new ** 2) <= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)

                #Координаты (0, +) (0, -)
                elif coordx == 0:
                    if (coordx_new ** 2 + coordy_new ** 2) >= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)
                        
                #Координаты (+, 0) (-, 0)
                elif coordy == 0:
                    if (coordx_new ** 2 + coordy_new ** 2) <= (coordx + n) ** 2 + (coordy + n) ** 2:
                        append_coords (coordx, coordy, a, r, google_bot)
                

                #Шаг 150 метров
                r += 0.003

            #Удаление повторов, вывод улиц
            m = set (a)
            street = str (m) [1:-1]
            bot.send_message (last_chat_id, 'Вокруг отправленных координат находятся улицы: {}'.format(street))

        else:
            bot.send_message (last_chat_id, 'Доброго времени суток, {}! Введите координаты и радиус, где искать.'.format (last_chat_name))

        #Обновление оффсета, потому что он должен отличаться от предыдущего
        new_offset = last_update_id + 1
        
if __name__ == '__main__':
    try:
        main ()
    except KeyboardInterrupt:
        exit ()

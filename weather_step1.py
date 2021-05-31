import requests
import settings


def weather_by_city(city_name):
    weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params_wather = {
        "key": settings.API_KEY,
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }

    # requests.get - запришавает и выдает данные
    #  полученные от:(weather_url), в данном случае в result
    # заложили в params (исходяшие параметры для запроса requests)
    # в данные словаря params_wather
    result = requests.get(weather_url, params=params_wather)

    # т.к. в result мы получим Текстовые данные, а нам надо в виде
    # списокв и словарей, то преобразуем его в формат json
    # метод предумострен requests
    weather = result.json()

    # ОБЯЗАТЕЛЬНО В БУДУЩЕМ ДОБАВИТЬ ИСКЛЮЧЕНИЕЯ НА ВЫПАД СЕРВЕРА
    # ПРОПАЛ ИНТЕРЕНТ, САЙТ ПОГОДЫ ОТВЕТИЛ НЕ ТО...
    '''
    Чтобы сервер не падал - задаем проверку на получение данных

    'data' - самый вернхний (первый) параметр, что мы получаем
    - поверяем, попал ли он в переменную weather
    нет - выдаем False

    current_condition - второй параметр, он есть?
    нет? - на первый False

    В объекте-словаре есть и data и в ней current_condition,
    а вдруг получили на вход не строку, как задумали?
    - пытаемся получить и проверяем само значение по ключу,
     что оно список - задав Индекс [0]
    Если получилось - ты получили свои данные
    Если нет получим False №2
    Описываем возможные ошибки
     - IndexError - нет списка нет индекса
     - TypeError - что-то есть, но тип не список
    '''

    if 'data' in weather:
        if 'current_condition' in weather['data']:
            try:
                return weather['data']['current_condition'][0]
            except(IndexError, TypeError):
                return False

    return False


if __name__ == "__main__":
    w = weather_by_city('Petersburg,Russia')
    print(w)

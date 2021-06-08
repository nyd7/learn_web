# Такой импорт дает нам возможность обрщаться к Фласку!,
# как текущему веб приложению
# вместо  import webapp.settings или .config
from flask import current_app

import requests


def weather_by_city(city_name):

    # weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    weather_url = current_app.config['WEATHER_URL']

    # "key": webapp.settings.API_KEY, - ранее
    # "key": current_app.config['WEATHER_API_KEY'] - сейчас
    # Ключ: ТекущееПриложение.Конфигурация[Переменная как ключ словаря!]

    params_wather = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }

    try:
        result = requests.get(weather_url, params=params_wather)
        result.raise_for_status()
        weather = result.json()

        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False
    return False


if __name__ == "__main__":
    w = weather_by_city('Petersburg,Russia')
    print(w)

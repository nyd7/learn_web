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

    '''
    Отлавивливаем 2 исключения
    1. Когда нет соединения с сайтом (нет интернета)
    В этом случае ошибка проявиться в строке requests.get(..,
    т.к. именно там идет запрос внешних данных
    requests погонит запросы по своим библиотекам и в итоге выдаст
    requests.exceptions.ConnectionError:...
    Делаем на это исключение, на все ошибки requests-а:
        except(requests.RequestException)
    помещаем весь блок с запросом в try
    а. Печатаем для себя сообщение, что Сетевая ошибка
    б. т.к. приосходит выход из всей функции - мы должны что-то вернуть
    возвращаем: return False
    Этот False у нас потом отыгрвается в server.py
    Нижний False, это общий, на случай, если не сработают if-ы

    2. Возможна ошибка в неправильном заведении url адреса,
    в weather_url
    В этом случае requests.get(... сделает запрос и получит ответ,
    но это будет ответ: 404 - Страница не найдена
    После requests попробует декодировать информацию в json
    = result.json(), но у него не получиться и выйдет ошибка
    json.decoder.JSONDecodeError:...
    по логике мы должны перехватить именно эту ошибку, но для
    этого нужно импортировать модуль json
    (т.е. не считается общей ошибкой requests)
    НО. Мы пошли другим путем, и добавили в исключения
    ValueError
    requests это поймет, что ему подсунули не те данные,
    недекодируемые json.decoder
    т.е. проблема не в типе данных, а в корявом значении

    ВАЖНО!!!
    Если у нас происходит ошибка, и мы ее не обрабатываем исключением,
    то эта информация об ошибке со всей подногодной
    вылетает на экран пользователю.
    А так делать нельзя!!!
    В этом случае будешт ошибка:
    500 - на сервере произошла ошибка

    Уточнение:
    Подногодная выйдет пользователю при
    включенном debug=True на нашем сервере: app.run(debug=True)
    Т.е. ошибка войдет в переменную, и пойдут дальнейшие ошибки
    по цепечкам функций, и все это выйдет на экран.
    Если же debug=False, то сраница выдаст ошибку:
    Internal Server Error (вунтрення ошибка сервера, тоже 500)

    '''
    try:
        result = requests.get(weather_url, params=params_wather)

        '''
        Если будет ошибка 4ХХ или 5ХХ на стороне сайта источника,
        то чтобы знать об этом, сделаем встроенную отловку исключений
        по этому поводу - raise_for_status(), выдаст HTTPError
        '''
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

# Переименовали файл из server.py в __init__.py
# а также переместили все файлы с программой в созаднную нами
# папку  webapp
# Файлы __init__.py выполняются автоматически при импорте модуля,
# точнее мы сделали папку webapp модулем питона, поместив туда файл
#  __init__.py

# После перемещения и превращения webapp в модуль через химию с __init__.py
# наши импортируемые файлы стали вложенными файлами
# поэтому надо указыват их как метод модуля webapp
# Из webapp.Название файла импорт функции
from flask import Flask, render_template
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

"""
Улучшим инициализацию сервера
В нашем случае это функция, которая создает (инициализирует) Flask app
 (Фласк приложение), проводит работу по инициализации
  и возвращает объект app (приложения).
Такой подход позволит упаковать всю работу по инициализации
 (созданию) сервера внутрь функции.
"""
# Пишем функцию "Создать Приложение"


def create_app():

    app = Flask(__name__)

    # Скажем фласку, откуда брать файл конфигурации,
    # в котором у нас стандратные настройки, ключи,
    #  значения по умолчанию и т.д.
    # Наше приложение.Конфигурация.ИЗ_ЭтоФайлПитона(Название нашго файла)
    app.config.from_pyfile('config.py')

    @app.route("/")
    def first_foo():
        page_title = 'Новости Python'

        # weather = weather_by_city('Petersburg,Russia')
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        # Наше приложение.Конфигурация.Переменная как ключ словаря!

        news_list = get_python_news()
        return render_template('index.html', weather=weather, page_title=page_title, news_list=news_list)

    # Вернуть Приложение
    # точнее все то, что получилось у нас после обработки
    # переменной app
    return app

# Новая команда для запуска:
# export FLASK_APP=webapp && export FLASK_ENV=development && flask run

# Удаляем блок за ненадобностью
# if __name__ == "__main__":
#     app.run(debug=True)

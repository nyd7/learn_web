# Переименовали файл из server.py в __init__.py
# а также переместили все файлы с программой в созаднную нами
# папку  webapp

from flask import Flask, render_template

# Импортируем Модуль db со свойствами (SQLAlchemy из flask_sqlalchemy)
# в котором у нас есть Моедль News
from webapp.model import db, News

# from webapp.python_org_news import get_python_news - больше не требуется

from webapp.weather import weather_by_city


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Активируем в нашем приложении уже настроенный модуль db,
    # с моделью News
    # Модуль db,с моделью News (База данных).
    #       подключись_к_приложению(Прилжение в переменной app)
    # в этот момент flask_sqlalchemy полезет в config.py
    # узнать место хранения базы
    db.init_app(app)

    @app.route("/")
    def first_foo():
        page_title = 'Новости Python'

        # weather = weather_by_city('Petersburg,Russia')
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        # Наше приложение.Конфигурация.Переменная как ключ словаря!

        # Ранее мы получали словарь и выводитил его в шаблон,
        #  и там обрабатывали
        # news_list = get_python_news()
        # Сейчас говорим
        # = База данных News.Запросить.Всё
        # news_list = News.query.all()
        news_list = News.query.order_by(News.published.desc()).all()
        # .order_by() - сортировать по.. полю (колонке)
        #  News.published - поле дата публикации
        #  .desc() - в обратном порядке

        return render_template(
                'index.html', weather=weather,
                page_title=page_title, news_list=news_list)
    return app

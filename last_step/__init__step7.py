# Переименовали файл из server.py в __init__.py
# а также переместили все файлы с программой в созаднную нами
# папку  webapp

from flask import Flask, render_template

from webapp.model import db, News
from webapp.weather import weather_by_city

# Из файла forms импортируем настроенный подкласс LoginForm
from webapp.forms import LoginForm


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def first_foo():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()

        return render_template(
            'index.html', weather=weather, page_title=page_title,
            news_list=news_list)

    # После получения урл запроса '/login' - запустить функцию
    @app.route('/login')
    def login():
        title = "Авторизация"
        # login_form делаем объектом подкласса LoginForm (см. файл forms.py),
        # со всеми его совйствами
        login_form = LoginForm()
        # Передать данные в шаблон и вернуть страницу
        # Шаблон login.html, принимаемые шаблоном переменные =...
        return render_template('login.html', page_title=title, form=login_form)

    return app

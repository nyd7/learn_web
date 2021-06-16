# Переименовали файл из server.py в __init__.py

# Подключим поддержку Flask-Login в приложении
# Импортируем LoginManager - объект Фласка,
# который будет управлять всеми процессами логина
from flask_login import LoginManager

from flask import Flask, render_template

# Добавили модель User, с помощью ее будем проверять,
# что к нам идет дейтсвительно правильный пользователь
from webapp.model import db, News, User

from webapp.weather import weather_by_city
from webapp.forms import LoginForm


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # Обренули в переменную login_manager Класс LoginManager
    login_manager = LoginManager()
    # "Делаем init передавая ему апликейшен"
    # Передаем менеджеру в управление наше приложение, воссоединяем их
    # Запускаем LoginManager в приложении app
    login_manager.init_app(app)
    # "Говорим как называется функция которая занимается логином
    # и паролем пользователя" (def login)
    login_manager.login_view = 'login'

    # НЕПОНЯТНАЯ ХРЕНЬ!!!
    # Тащит из куки id пользователя
    # запрашивает его из базы данных
    # и по этому id вытаскивает конкретный объект User-а
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def first_foo():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()

        return render_template(
            'index.html', weather=weather, page_title=page_title,
            news_list=news_list)

    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    return app

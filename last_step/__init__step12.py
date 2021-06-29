# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
# Проводим Blueprint!

# Подключим Blueprint user в приложение
# имппоритруем переменную blueprint, которая
# является готовым (содержащий необходимые парметры) Blueprint-ом
# А именно экземпляром класса с заданными нами характеристиками
# в webapp.user.views. Переимновываем импортируемую переменную
# во временное имя user_blueprint. Т.к. в последующем мы будем
#  импортировать и дргуе Блюпринты, а Имена должны отлчаться
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint

from flask import Flask
from flask_login import LoginManager

from webapp.db import db
from webapp.user.models import User


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    # База, будь базой для приложения app, которое app = Flask(__name__)
    # База, работай вот с этим приложением. Но ты можешь быть базой
    # и для других приложений...
    # Аналогия от Михаила:
    # Если выходит дополнение к игре, то чтобы оно окзалось в игре
    # его надои инициализировать в игре
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Говорили как называется функция которая занимается логином
    # и паролем пользователя" (def login)
    # Она перехала в результате Блюпринта в модуль
    # юзер, поэтому вместо login будет user.login
    login_manager.login_view = 'user.login'
    # Присоединяем Блюпринт юзер к приложению.
    # Фласк-Приложение регстирует у себя Блюпринт,
    # что есть такой (имя, место, модуля и заданный кусок урл адреса)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)

    # НЕПОНЯТНАЯ ХРЕНЬ!!!
    # По id вытаскивае весь объект Пользователь
    # Потом будем часто пользоваться
    # Тащит из куки id пользователя
    # запрашивает его из базы данных
    # и по этому id вытаскивает конкретный объект User-а
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

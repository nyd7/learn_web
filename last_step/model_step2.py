# ПЕРЕНЕСЛИ все модели из webapp модели в user модели
# те, что относятся к user, остальное чистим.

# Предварительно устнаовив pip flask_login
# имортируем из него UserMixin, которы содержит доп свойства
# по отражению пользователя, а именно
# is_authenticated: True
# is_active: True
# is_anonymous: Flask-Login выставит это свойство в True,
#  если пользователь не авторизован
#  get_id(): метод, который возвращает id пользователя в виде строки,
# нам бы пришлось делать его если бы в Модели User,
# id называось иначе чем id (к примеру user_id)
# Подробности см в лекции.
from flask_login import UserMixin

# Бибилотека с шифраторами
#  generate_password_hash - хеширует пароль пользователя
#  check_password_hash - получает пароль при очередном входе пользователя,
# снова хеширует через generate_password_hash и проверяет на совпадение
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        # return '<News {} {}>'.format(self.title, self.url)
        return f"News {self.title} {self.url}"


# ДОбавим к классу User еще наследоство и от UserMixin
# наследоваться можно от нескольких классов
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    # Добавим еще 2 свойства для работы с паролями
    # Функция шифрует пароль
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Функция шифрует и сравнимвает при потоврном входе пользователя
    # и возращает итого проверки Правда или Ложь
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Класс должен сообщать нам, является ли пользователь администратором
    # Добавим в классе User метод is_admin.
    # Декоратор @property позволяет вызывать метод как атрибут, без скобочек:
    # т.е. не is_admin(), а is_admin
    #
    # Пишем функцию, которая сравнивает значение self.role и 'admin'
    # и выдает ЛОЖЬ или ПРАВДА
    @property
    def is_admin(self):
        return self.role == 'admin'

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
# Из фалска SQL импортируем модуль SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Объявляем переменную db как модуль SQLAlchemy
#  db становтиься изменяемым модулем.
db = SQLAlchemy()

# Переменная News будет подклассом унаследованным,
# от класса Model в модуле SQLAlchemy = db.Model
# Также. Ранее мы из sqlalchemy.orm имортировали функции Column,
#  Integer, String
# здесь же, ришили описывать по типу sqlalchemy.orm.Column...
# + добавилось .DateTime (дата) и .Text (текст)
# primary_key - является уникальным ключом
# nullable=False - поле может быть пустым = Ложь, иначе выдаст ошибку

# Прописывая нюансы в подмоделе News мы меняем глбальную модель db,
# которая сама унаследовалась от SQLAlchemy()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        # return '<News {} {}>'.format(self.title, self.url)
        return f"News {self.title} {self.url}"


# Создали модель (табилцу) пользователя
# Что такое index=True пока не известно
# но нужно здавать это тем колонкам, по которым чаще всего будем
# искать или фильтровать. index ускоряет это процесс
# role - роль, юзер или админ
#
# ДОбавим к классу User еще наследоство и от UserMixin
# наследоваться можно от нескольких классов
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

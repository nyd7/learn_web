# ПЕРЕНЕСЛИ все модели из webapp модели в user модели
# те, что относятся к user, остальное в глобальном models,
# или разнесено по Блюпринтам  глабоальная удалена.

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# db=SQLAlchemy переносить не стали, а импотировали эту переменную,
# т.к. она означает общую форму баз данных, которую можно использовать
# для создания прочих разных моделей
from webapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_admin(self):
        return self.role == 'admin'

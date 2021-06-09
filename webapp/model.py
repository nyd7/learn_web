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

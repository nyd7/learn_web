from webapp.db import db
from datetime import datetime
from sqlalchemy.orm import relationship


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    # Хотим считать кол-во комментариев к каждой новости
    # Для этого добавим метод в класс News
    # Будем вызывать его в шаблоне index.html
    # Комментарии: {{ news.comments_count() }}
    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self):
        return f"News {self.title} {self.url}"


# Создаем модель для комментариев
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    # default= - значение по умолчанию
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True
    )
    # ForeignKey - указываем, что это внешний ключ
    # 'news.id' - внешний ключ,
    #  С маленькой буквы пишем т.к. хоть модель и с большой
    #   - в базе создается таблица - с маленькой буквы
    # ondelete='CASCADE' - если новость будет удалена
    #  - то удалять все комментарии к ней

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    # Мы создаем переменную news, которая будет вести модели News
    #  backref= - созадаст уже в модели News виртуальное доп поле
    #  "comments", к которому мы сможем также обращаться через News
    # т.е. создав поле здесь - мы создали поле и в другой модели
    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

# Допольнительно импортируем current_app - текущее приложение
# Т.е. наше приложение пойдет за новостями сюда,
# и current_app индетефицирует его, и после мы по этому
# условию сможет зайти в config этого приложения
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user
from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import Comment, News
from webapp.weather import weather_by_city

blueprint = Blueprint('news', __name__)
# Т.к. это главная страница, то префикса url_prefix
# для blueprint-а не делаем


@blueprint.route("/")
def index():
    page_title = 'Новости Python'
    # Чтобы достать настройки из конфигурации, используем
    # current_app (см. модуль в шапке)
    # Вместо app.config['WEA будет current_app.config['WEA
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    # Здесь мы выводим все новости,
    # даже если еще не успели собрать для них текст
    # news_list = News.query.order_by(News.published.desc()).all()

    # Добавим условие, что нужно фильтровать, если текст новости
    # не пустой .filter(News.text.isnot(None))
    news_list = News.query. \
        filter(News.text.isnot(None)). \
        order_by(News.published.desc()). \
        all()

    # Т.к. мы сделали наследование в шаблоне - уточняем адрес здесь
    # вместо 'index.html' будет 'news/index.html'
    return render_template(
        'news/index.html',
        weather=weather,
        page_title=page_title,
        news_list=news_list
    )


# Срабатывает, если прошло обращение новости/номер новости
# преобразование в целое число в html офомрляется <int:news_id>
@blueprint.route('/news/<int:news_id>')
# за нас фласк вытащит news_id из урл, не паримся
def single_news(news_id):
    # Запрашиваем новость по номеру в базе
    my_news = News.query.filter(News.id == news_id).first()
    # Если вышла ошибка
    if not my_news:
        # Предварительно импортировали,
        # который по науке выдает ошибку на страницу
        # Вычисление прерывается
        abort(404)

    # Добавляем форму для возможности заполнения комментариев,
    # и передаем ее в шаблон
    form = CommentForm(news_id=my_news.id)
    # В самой CommentForm форме news_id - это скрытое поле.
    # Т.е. значения в него никак пользователь не передаст.
    # Когда же мы попадаем в запрос single_news, то мы уже знаем
    # какой news_id запошен пользователем (см. фукцию целиком)
    # Т.о. мы на этом этапе передаем полю формы news_id значние
    # id из строки my_news, которая получена из базы

    # Иначе передаем данные в шаблон 'news/single_news.html
    return render_template(
        'news/single_news.html',
        page_title=my_news.title,
        news=my_news,
        comment_form=form
    )
# my_news - это объект/строка, т.е. пока не конретно текст


# Делаем обработчик для формы комментариев
@blueprint.route('/news/comment', methods=['POST'])
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        if News.query.filter(News.id == form.news_id.data).first():
            comment = Comment(
                text=form.comment_text.data,
                news_id=form.news_id.data,
                user_id=current_user.id  # id текущего пользователя
            )

            db.session.add(comment)
            db.session.commit()
            flash('Комментарий успешно добавлен')
    # Комментарии нижней части аналогичны
    #  user-views-blueprint.route('/process-reg'...
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в заполнении поля "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(request.referrer)
    # redirect - перенапрвить
    # request - хранилище данные полученных из запроса
    # .referrer - данные с какой страницы пришел запрос
    # Итого перенеправляем польз-ля на страницу обратно

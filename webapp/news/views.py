# Допольнительно импортируем current_app - текущее приложение
# Т.е. наше приложение пойдет за новостями сюда,
# и current_app индетефицирует его, и после мы по этому
# условию сможет зайти в config этого приложения
from flask import Blueprint, render_template, current_app
from webapp.news.models import News
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
    news_list = News.query.order_by(News.published.desc()).all()

    # Т.к. мы сделали наследование в шаблоне - уточняем адрес здесь
    # вместо 'index.html' будет 'news/index.html'
    return render_template(
        'news/index.html', weather=weather, page_title=page_title,
        news_list=news_list)

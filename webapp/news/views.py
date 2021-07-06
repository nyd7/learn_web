# Допольнительно импортируем current_app - текущее приложение
# Т.е. наше приложение пойдет за новостями сюда,
# и current_app индетефицирует его, и после мы по этому
# условию сможет зайти в config этого приложения
from flask import abort, Blueprint, render_template, current_app
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
    # Здесь мы выводим все новости,
    # даже если еще не успели собрать для них текст
    # news_list = News.query.order_by(News.published.desc()).all()

    # Добавим условие, что нужно фильтровать, если текст новости
    # не пустой .filter(News.text.isnot(None))
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()

    # Т.к. мы сделали наследование в шаблоне - уточняем адрес здесь
    # вместо 'index.html' будет 'news/index.html'
    return render_template(
        'news/index.html', weather=weather, page_title=page_title,
        news_list=news_list)


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
    # Инвче передаем данные в шаблон 'news/single_news.html
    return render_template('news/single_news.html',
                           page_title=my_news.title, news=my_news)
# my_news - это объект/строка, т.е. пока не конретно текст

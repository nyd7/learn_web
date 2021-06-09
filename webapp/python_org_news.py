from datetime import datetime
import requests
from bs4 import BeautifulSoup
from webapp.model import db, News


def get_html(url):

    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news():

    html = get_html("https://www.python.org/blogs/")

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find('ul', class_='list-recent-posts').findAll('li')

        for news in news_list:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text

            try:
                published = datetime.strptime(published, '%B %d, %Y')
            except(ValueError):
                published = datetime.now()

            save_news(title, url, published)

    return False


def save_news(title, url, published):
    # ВНИМАНИЕ. т.к. у нас в url стоит проверка unique=True
    # (чтобы были уникальны), то при попытки заполнить базу повторно
    #  вылезет большая ошибка sqlalchemy.exc.IntegrityError,
    #  что неможет запольнить unique и т.д...
    #
    new_news = News(title=title, url=url, published=published)

    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:

        db.session.add(new_news)
        db.session.commit()

# news_exists = News.query.filter(News.url == url).count()
# if not news_exists: - если НЕ является ИСТИНА (т.е. 0 (ИСТИНА это это не0))
# news_exists - переменная кот. будет хранить кол-во совпадений
# News - наша базы данных с данными
# .query - запросить информацию из базы данных
#  .filter() - по конкртеному параметру
# (News.url - смотрим параметр url по всей колонке
# == url) - равно текущему полученному с сайта url для записи
#  .count() - считаем

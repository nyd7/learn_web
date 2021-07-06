# Здесь кол используемый всеми парсерами
# Взяли блоки из файлика python_org_news.py

import requests
from webapp.db import db
from webapp.news.models import News


def get_html(url):
    # User-Agent - меняем свое имя в запросе, чтобы не забанили.
    # узнаем User-Agent свого браузера (как - смотри в Трелло)
    # и задаем в переменную headers, ее в атрибуты запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_news(title, url, published):
    new_news = News(title=title, url=url, published=published)

    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:

        db.session.add(new_news)
        db.session.commit()

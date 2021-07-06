from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news

import locale
# Дает информацию о платформе (оперкционной системе)
import platform


# Мы получаем и выдаем дату на русском,
# то и определим систмные локалии как русские
if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
elif platform.system() == 'Linux':
    locale.setlocale(locale.LC_ALL, "ru_RU.UTF8")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


# Переведем "вчера" и "сегодня" в дату
def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()


# Получение новостей с Хабра, все колонки, кроме самой страницы новостей
# В конце сохраняем
def get_news_snippets():

    html = get_html(
        "https://habr.com/ru/search/?target_type=posts&q=python&order")

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find(
            'ul', class_='content-list_posts').findAll(
                'li', class_='content-list__item_post')

        for news in all_news:
            title = news.find('a', class_='post__title_link').text
            url = news.find('a', class_='post__title_link')['href']
            published = news.find('span', class_='post__time').text
            published = parse_habr_date(published)
            save_news(title, url, published)


# Получение текста из самой страницы новостей,
# и сохранение во время перебора тех, у кого еще не заполнен текст
def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    # .is_(None) - если поле пустое

    # Получили объект со всеми новостями, где поле текста - пустое
    for news in news_without_text:
        # html = венрнуть содержание страницы объект строка news.колонка url
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            print(news.url)
            print('------------------------------------------------')
            article = soup.find('div', class_='post__text').decode_contents()
            # .decode_contents() - вернет на данные в виде html кода.
            # Ранее мы запросили html страницы и преобразовали все в текст,
            # чтобы обработать супом. Сейчас же трансофрмируем обратно, чтобы
            # сохранить всю красоту оформления.
            # Если ошибки нет
            if article:
                # В стоку news, колонку text записывам данные.
                # Пишем прям на месте, т.к. объект у нас сейчас в работе
                news.text = article
                db.session.add(news)
                db.session.commit()

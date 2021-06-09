from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Импортируем из файла model Модудль db и Модель News
# для написания функции для записи новости в БД
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
        # Больше не нужен, будем хранить в базе данных
        # result_news = []
        for news in news_list:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            # Ранее дату вытаскивали текстом,
            # сейчас пробуем перевести ее в дату, а если не выходит,
            # то пока вернем текущую дату
            # что текущий текстовый формат '%Y-%m-%d  псомотрели в оригинале
            # см. материалы по datetime, в т.ч. strptime
            try:
                published = datetime.strptime(published, '%B %d, %Y')
            except(ValueError):
                published = datetime.now()

            # Созараняем полученные данные в базу данных
            save_news(title, url, published)

            """
            Теперь мы собираем данные не в словарь, а записываем в базу данных
            с помощью нашей функции save_news()
            result_news.append({
                'title': title,
                'url': url,
                'published': published
            })
        return result_news
            """
    return False


# Создаем функцию по сохранению новостей в базу данных

# Объявяем переменную new_news, как объект по модели News,
# ="Создали объект класса News"
# и в нее обязательно нужно записать 3 параметра: title, url, published
# т.к. id заполняется автоматически, а text можно оставлять пустым,
# да и пока что мы с ним не работаем.

# Почему пишем title=title, url=url, published=published ???
# у нас же нет данных, чему = title, url, published,
# это были локальные аргументы внутри функии и исчезли...
# Ответ: мы вствили save_news в функцию get_python_news,
# где получаем эти переменные/аргументы


def save_news(title, url, published):
    new_news = News(title=title, url=url, published=published)

    # Кладем данные/изменения в сессию db
    db.session.add(new_news)

    # Фискируем (записываем) изменения в базу данных
    db.session.commit()

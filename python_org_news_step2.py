import requests
from bs4 import BeautifulSoup

# !!! В данном случае у нас 2 функции, и если мы будем это передвать
# на сервер, чтобы транслировать новости, то
# их обе нужно будет прописывать в файле сервера, а нам хочется одну,
# в связи с этим, будем делать следующий шаг
# - Объединение в одну функцию


def get_html(url):

    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news(html):

    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.find('ul', class_='list-recent-posts').findAll('li')
    result_news = []
    for news in news_list:
        '''
        Находим в news блок тега а, и из него извлекаем текстовые атрибуты '''
        title = news.find('a').text
        '''
        К нетекстовым атрибутам орбращаемся, как к элментам словаря'''
        url = news.find('a')['href']
        published = news.find('time').text
        '''
        Заводим все новости в список словарей
        Каждый новый словарь дополнятеся в список по циклу
         и содержит одни и те же ключи,
         но подтягиваются новые данные, из цикла.
        '''
        result_news.append({
            'title': title,
            'url': url,
            'published': published
        })

    return result_news


if __name__ == "__main__":
    html = get_html("https://www.python.org/blogs/")
    if html:
        print(get_python_news(html))

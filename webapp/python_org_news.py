import requests
from bs4 import BeautifulSoup


def get_html(url):

    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news():
    # Убрали из get_python_news обязательный аргумент html
    # и венсли значение в саму функцию, сделали ее нечистой...
    # Также, мы теперь функцию get_html вызваем изнутри
    # функции  get_python_news
    html = get_html("https://www.python.org/blogs/")

    # Переносим проверку на то, что get_html не выдал False, сюда
    # ранее была под if __name__ == "__main__":
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in news_list:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            result_news.append({
                'title': title,
                'url': url,
                'published': published
            })
        return result_news
    return False

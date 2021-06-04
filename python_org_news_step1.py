import requests
from bs4 import BeautifulSoup


def get_html(url):

    '''
    Пытаемся
    Запрашиваем данные сайта в переменную result
    Если получили ответ типа 4ХХ или 5ХХ
     то вызовем тип ошибки requests.RequestException
     которую обработает except
    Вернуть полученные данные в виде текста, но если на сайте
     прошла ошибка, выдан нелогичный запросу текст, то
     сработает ошибка типа ValueError (НАДО УТОЧНЯТЬ!!!)
    '''

    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text

    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news(html):

    '''
    Преварщаем переменую soup в елемнт BeautifulSoup
     html - входящая перменная в которй записан html текст
     html.parser - преобразователь html в дерево разбора
    soup.find() - ищем
     первый поавшийся ul
     в котором class_ содержит слова 'list-recent-posts'

    '''
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.find('ul', class_='list-recent-posts').findAll('li')
    # news_list = news_list.findAll('li')
    #  - уточняем поиск на поиск всех li'
    # но сделали это путем применения метода к уже полученным данным
    # делаем уточнение на основной функции, дописываем .findAll('li')
    print(news_list)


if __name__ == "__main__":
    html = get_html("https://www.python.org/blogs/")
    if html:
        '''
        В целях обучения, просмотра, запишем итог в файл python-org-news.html
        Далее мы это звено цепи уберем, и будем работать непосрдестванно
        с html
        '''
        with open("python-org-news.html", "w", encoding="utf8") as f:
            f.write(html)

        get_python_news(html)

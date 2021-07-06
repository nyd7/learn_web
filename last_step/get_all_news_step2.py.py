from webapp import create_app
from webapp.news.parsers import habr

app = create_app()
with app.app_context():
    # habr.get_news_snippets()
    habr.get_news_content()

# Удаляем файл, т.к. функцию сбора выполняет наш планировщик, файл tasks.py

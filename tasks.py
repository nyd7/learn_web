# Планировщик (см. Трелло)
from celery import Celery
# Таймер Celery
from celery.schedules import crontab
# Функция по созданию приложени, для запуска из контекста
from webapp import create_app
# Тянем весь парсер новостей с Хабра
from webapp.news.parsers import habr

# Не пишем просто app для кого-то из них, чтобы не было конфликтов
celery_app = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()
# ('tasks', - должно совпадать с названием текущего файла,
# нужно для корректно запуска модуля


# Получение новостей с Хабра
# Оборачиваем в Celery
@celery_app.task
def habr_snippets():
    # Октрываем сессию в режиме контекста
    with flask_app.app_context():
        # Запускаем .функцию из файла habr
        habr.get_news_snippets()


# Получение текста из самой страницы новостей
@celery_app.task
def habr_content():
    with flask_app.app_context():
        habr.get_news_content()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), habr_snippets.s())
    sender.add_periodic_task(crontab(minute='*/2'), habr_content.s())

# @celery_app.on_after_configure.connect
# - мы подключим функцию ниже после того,
# как Селери сделает connect (подлкючиться) к очереди,
# и будет готова к решению задач
# А очередь у нас храниться отдельно, даже в выключеном состоянии
# в брокере redis
# --------------
# elery_app - запускаем Celery
# on_after_configure - Сигнал отправляется после того,
# как приложение подготовило конфигурацию,
# connect - подключить

# setup_periodic_tasks
# - Функция которая будет создавать расписание
# sender - отправитель,
# "та штука с помощью которой мы можем управляь Celery изнунтри нашей функции"
# **kwargs - произвольное число именованных аргументов.
# add_periodic_task - добавить задачу
# crontab - периодичность
# minute='*/1' - раз в минуту
# habr_snippets - запускаемая функция, задача
# .s() - запустить функцию

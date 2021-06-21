# Модуль getpass по сути тоже самое, что input,
# но для ввода пароля, чтобы нельзя было увидеть, что
# вводит пользователь
from getpass import getpass

# Систменый модуль, будем использовать в нем функцию exit,
# т.к. не захотим возращать данные или ответ, а просто выйти
import sys

# Из приложения импортируем функцию по созданию
# и запуску приложения
from webapp import create_app

# Из модели имортируем Модель юзера и глобальную Модель db
# from webapp.model import User, db
from webapp.db import db
from webapp.user.models import User


# Воссоздали в перменной наше приложение
app = create_app()

# Через контекст к переменной app получили доступ к элментам функции create_app
# Открыли приложение для работы
with app.app_context():
    # Просим пользователя ввести Имя пользователя
    username = input('Введите имя пользователя: ')
    # Считаем, скольо у нас таких пользователй с таким имененм в базе
    # Если 1 (Истина) уже есть, то выдаем ошибку и выходим.
    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    # Просим через пользоватлея через getpass дважды ввести пароль
    # и проверяем на совпадение. Если нет, то выходим.
    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit(0)

    # Если прошли все проверки, т.е. не вышли по sys.exit(0), то
    # создаем пользователя
    # Переменная класса User.username = username введнной пользвателем
    # Роль всем даем как Админ, но можно заморочится
    # и придумать свои условия, и проверки на это условие
    new_user = User(username=username, role='admin')
    # Класс User у нас же содериать функцию по кешированию пароля
    new_user.set_password(password)

    # Теперь объект класса new_user - User польностью заполнен,
    # передаем его на сохранение в базу данных

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))

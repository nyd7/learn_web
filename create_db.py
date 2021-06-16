# Создали файл именно в КОРНЕ приложения

# Импоритриуем уже модуля webapp
#  db - это настроенный Модуль (SQLAlchemy из flask_sqlalchemy)
#  с Моедлью News
#  основную фунцию по созданию Приложения create_app

from webapp import db, create_app

# Говорим
# Модуль db, с Моеделью News.Создай все,
#      что у тебя есть(в приложении = которое созадется при create_app)
# "db создай все модельки для этого апликейшина"
#
# Настроенная база данных db"SQLAlchemy".Создайся(Запустись через
# контекст функции create_app из webapp
# Т.е. в __init__.py мы ФласкПриложение подружили с базой db"SQLAlchemy".
# но чтобы Приложение видело то,
#  что создается в базе именно для этого Приложения
#  - мы должны запустить создание этой базы изнутри этого Приложения
# Т.к. мы можем иметь одну базу для разных приложений

db.create_all(app=create_app())

# Альтернатива из интернета:
# def my_function():
#     with app.app_context():
#         user = db.User(...)
#         db.session.add(user)
#         db.session.commit()

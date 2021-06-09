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

db.create_all(app=create_app())

# ПЕРЕНЕСЛИ все модели из webapp модели в user модели
# те, что относятся к user, остальное чистим.
# Переиминовали файл из model.py в db.py,
# и везде где писали model меняем на db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

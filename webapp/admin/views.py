# Перносим сюда route-ы и заменяем Приложение на Блюпринт
# app на blueprint

from flask import Blueprint, render_template
# # Создали декоратор admin_required, поэтому меизмеяем няем функцию
# from flask_login import current_user, login_required
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__, url_prefix='/admin')

# # Создали декоратор admin_required, поэтому меизмеяем няем функцию
# # Зачемно убираем здесь admin, т.е. вместо '/admin' будет '/'
# @blueprint.route('/')
# @login_required
# def admin_index():
#     if current_user.is_admin:
#         return 'Привет админ'
#     else:
#         return 'Ты не админ!'


# Т.к. добавили адинмку страницу - меняем return
@blueprint.route('/')
@admin_required
def admin_index():
    # return 'Привет админ!'
    title = 'Панель управления'
    return render_template('admin/index.html', page_title=title)
    # Передаем данные в шаблон по адресу admin/index.html

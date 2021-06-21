# Перносим сюда route-ы и заменяем Приложение на Блюпринт
# app на blueprint

from flask import Blueprint
from flask_login import current_user, login_required


blueprint = Blueprint('admin', __name__, url_prefix='/admin')


# Зачемно убираем здесь admin, т.е. вместо '/admin' будет '/'
@blueprint.route('/')
@login_required
def admin_index():
    if current_user.is_admin:
        return 'Привет админ'
    else:
        return 'Ты не админ!'

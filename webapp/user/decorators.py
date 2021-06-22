# Берем код из библиотеки Фласка на ГитХаб
# https://github.com/maxcountryman/flask-login/blob/master/flask_login/utils.py#L231
# Копируем фунцию проверки @login_required - Дикоратор проверяет,
# что это авторизированный пользователь и если нет,
#  то вернет его на главную странцу
# Вставляляем все необходимые импорты (подобраби)

from functools import wraps
# Понадобился для создания @wraps(func), про который не рассказали...

from flask import current_app, flash, request, redirect, url_for
from flask_login import config, current_user


# Переиминовали login_required в admin_required
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        # Добавили собственный код проверки на админа
        elif not current_user.is_admin:
            flash('Эта страница доступна только админам')
            return redirect(url_for('news.index'))
        # ---
        return func(*args, **kwargs)
    return decorated_view

# Перносим сюда route-ы и заменяем Приложение на Блюпринт
# app на blueprint

#  После всех переносов добавили импорт Blueprint
# Blueprint объявлет названание Блюпринта и его урл-префикс
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

# Добавляем нашу произволно придуманную RegistrationForm
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

# Переменная blueprint =
#  Объявление Blueprint(название папки/Blueprint-а, имя текущего файла,
# урл для этого Blueprint-а)
# Теперь весе маршруты внутри этого Blueprint-а будут иметь в
# заголовке, вначале, кусок урл Blueprint-а - '/users'
# Меняем запуск из приложения на запуск с Blueprint-а
# Вместо @app.route('/login') будет @blueprint.route('/login')

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Авторизация"
    login_form = LoginForm()
    # Т.к. мы сделали наследование в шаблоне - уточняем адрес здесь
    # вместо 'index.html' будет 'user/login.html'
    return render_template('user/login.html', page_title=title,
                           form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            # Функцию index перенсли в созданный модуль news,
            # уточняем адрес
            return redirect(url_for('news.index'))
    flash('Неправильное имя пользователя или пароль')
    # После того как сделали Blueprint, т.е. переместили в т.ч. route,
    # который содержит функцию login(),
    # то соответсвено отсылка на функцию будет
    # Новый модуль"user".Искомая функция"login"
    # Вместо url_for('login') будет url_for('user.login')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились')
    return redirect(url_for('news.index'))

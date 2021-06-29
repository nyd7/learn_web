# Для работы с базой данных, при регистрации пользователя
# добавляем from webapp.db import db
from webapp.db import db

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

# Добавляем нашу произволно придуманную RegistrationForm
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


# Логин, проверка на существование пользователя и форма для заполнения
# Дашем форму получив запрос по урл /login', и принимаем в нее данные
# Реакция возникает при обращении по урл адресу
@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title,
                           form=login_form)


# Логин, обработчик формы Логина
# На эту обработку мы вышли из формы в шаблоне,
# та у нас прямое указание, что после заполнения активизаровать
# фукнцию содержающую название фукции process_login
@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('news.index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились')
    return redirect(url_for('news.index'))


# Страница для регистрации пользователей, получили запрос по урл
@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('user/registration.html',
                           page_title=title, form=form)


# Обработчик регистрации пользоватлей, получили по заполненной
# форме на странице для регистрации пользователей
@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='user'
            )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    # В форме мы создали Валидатор проверяющий при регистрации, что
    # такой пользователь уже существует, или такой емейл.
    # И при любой ошибке выходит сообщение
    #  flash('Пожалуйста, исправьте ошибки в форме')
    # Добавляем возможность смотреть, где конретно приозошла ошибка,
    # добавляем этот блок
    else:
        # Конструкция for field, errors in form.errors.items()
        #  form.errors.items()
        #  form - это данные заполненной формы (см. form = RegistrationForm())
        #  В полях формы у нас именнованные
        #  экземпры подклассов FlaskForm (username, password...)
        #  У FlaskForm есть метод errors, который записыает в себя ошибки, и
        #  выдает их, если есть таковая, когда срабатывает Валидатор
        #  Записыает в виде словаря Поле:Описание ошибки
        #  Свойство Словарей .items() дает нам возможность перебирать пары
        #  в цикле и получать раздельно ключ и значение for k, v in d.items():
        #
        #  В итоге мы проходим по форме, и собираем все ошибки.
        #  Проходим по словарю и вадаем текстом, что там есть
        for field, errors in form.errors.items():
            for error in errors:
                # Выдаем запись
                # getattr(form, field) превращается в form.field
                # Запрашиваем элемент формы form.field.label.text,
                # т.е. Форма.Поле(атрибут/username).Лейбл('Имя пользователя').
                #    выдать в виде текста
                #
                # Полученная запись об ошибке
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                    ))
        return redirect(url_for('user.register'))
    # flash('Пожалуйста, исправьте ошибки в форме')
    # return redirect(url_for('user.register'))

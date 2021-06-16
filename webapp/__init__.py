# Переименовали файл из server.py в __init__.py

from flask import Flask, render_template, flash, redirect, url_for
# Уберем возможность заходить на страницу /login для авторизованных
# добавляем  current_user
# Создадим страницу, доступную только зарегистрированным
# добавляем  login_required (это дикоратов)
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    # База, будь базой для приложения app, которое app = Flask(__name__)
    # База, работай вот с этим приложением. Но ты можешь быть базой
    # и для других приложений...
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # НЕПОНЯТНАЯ ХРЕНЬ!!!
    # По id вытаскивае весь объект Пользователь
    # Потом будем часто пользоваться
    # Тащит из куки id пользователя
    # запрашивает его из базы данных
    # и по этому id вытаскивает конкретный объект User-а
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    # В какой-то нежожиданный момент мы переименовали first_foo в index
    def index():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()

        return render_template(
            'index.html', weather=weather, page_title=page_title,
            news_list=news_list)

    @app.route('/login')
    def login():
        # В свое вермя мы унаследовали в Модель User из класса
        # фалска UserMixin, в котором есть переменная current_user и
        # его свойства в т.ч. is_authenticated = Правда, если пользователь
        # авторизирован
        # Если текущий пользователь атворизирован, то перенаправляем его
        # на главную страницу
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    # Реализуем обработку формы логина
    @app.route('/process-login', methods=['POST'])
    def process_login():
        # создаем экзмепляр (объект) формы
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            # Если user Истина (не 0, None) и Проверка пользователя прошла
            #   user.check_password(form.password.data)
            #    ВОЛШЕБНЫМ оразом переменная user стала обладать не только
            # именем пользователя, но и свойствами класса User,
            # откуда мы вызваем проерку пароля check_password(пароль из
            # только что заполненной формы)
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    # Выход пользователя из сессии под своим логином
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    # Дикоратор @login_required проверит, что это авторизированный
    # пользователь и если нет, то вернет его на главную странцу
    @login_required
    # admin_index допольнительно проверяет, что текущий пользователь
    #  не просто авторизирован, но и имеет роль админа, эту возможность
    # проверки мы учли в Моделе User, возвращает ЛОЖЬ или ПРАВДА
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'

    return app

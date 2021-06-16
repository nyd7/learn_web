# Переименовали файл из server.py в __init__.py

# Реализуем обработку формы логина
# импортируем login_user
from flask_login import LoginManager, login_user

# импортируем
# flash - позволяет передавать сообщения между route-ами
# redirect - делает перенаправление пользователя на другую страницу
# url_for - помогает получить url по имени функции,
#  которая этот url обрабатывает
from flask import Flask, render_template, flash, redirect, url_for

from webapp.model import db, News, User

from webapp.weather import weather_by_city
from webapp.forms import LoginForm


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
    def first_foo():
        page_title = 'Новости Python'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()

        return render_template(
            'index.html', weather=weather, page_title=page_title,
            news_list=news_list)

    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    # Реализуем обработку формы логина
    # Маршрут и какие методы будет обрабатывать этот route
    @app.route('/process-login', methods=['POST'])
    def process_login():
        # создаем экзмепляр (объект) формы
        form = LoginForm()
        # validate_on_submit соберет все данные из формы,
        #  запустит любые валидаторы,
        #  прикрепленные к полям, и если все в порядке вернет True
        # Мы уже импортировали LoginForm,
        # а до этого добавили волидаторы в forms
        if form.validate_on_submit():
            # Запрашиваем пользователя из базы данных
            # user= Модель.Запрос.Фильровать по (колонке username =
            #  (((form.username.data /Наша форма.переменная username
            #               .полученные данные в ней/)))
            # .Первое значение
            user = User.query.filter_by(username=form.username.data).first()
            # Если user Истина (не 0, None) и Проверка пользователя прошла
            #   user.check_password(form.password.data)
            #    ВОЛШЕБНЫМ оразом переменная user стала обладать не только
            # именем пользователя, но и свойствами класса User,
            # откуда мы вызваем проерку пароля check_password(пароль из
            # только что заполненной формы)
            if user and user.check_password(form.password.data):
                # Залогиним пользователя
                login_user(user)
                # Выдаем сообщение
                flash('Вы вошли на сайт')
                # Перейти на странцу(Получить урл
                #  где применяется функция(index))
                # ОДНАКО у нас НЕТ функции  index,
                # Есть страница index
                return redirect(url_for('index'))
        # Если комбинация выше не прошла, то выдаем сообщение
        flash('Неправильное имя пользователя или пароль')
        # Перейти на странцу(Получить урл где прменяется функция login
        # Так перейдем на страницу '/login'
        return redirect(url_for('login'))

    return app

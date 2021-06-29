# ПЕРЕНЕСЛИ все формы из webapp forms в user forms
# webapp forms - удалили, т.к. кроме пользовательских
# форм у нас больше нет


from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
"""
Добавим пару стандартных валидаторов
Мы уже использовали валидатор DataRequired,
который проверял, что поле не пустое.
Добавим валидаторы Email и EqualTo - они проверяют,
что в поле введен email (Email)
и что значение одного поля идентично значению другого (EqualTo):

from wtforms.validators import DataRequired, Email, EqualTo

Дополнительные проверки
Если пользователь при регистрации укажет имя,
которое уже есть в системе,
то мы получим ошибку базы данных.
Добавим собственные валидаторы для полей формы.!!!
Валидатор - это просто метод класса формы,
имя которого строится как validate_ПОЛЕ (нижнее подчеркивание),
например validate_email.
В случае ошибки валидатор должен
выкидывать исключение wtforms.validators.ValidationError
Импортируем ValidationError
А также импорируем Объект класса User (он же подкласс)
from webapp.user.models import User
"""
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    remember_me = BooleanField('Запомнить меня', default=True,
                               render_kw={"class": "form-check-input"})

    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-primary"})


# Создаем форму для регистрации пользователя по аналогии со страницей входа
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})

    # Добавляем почту
    email = StringField('Email', validators=[
                        DataRequired(), Email()],
                        render_kw={"class": "form-control"})

    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})

    # Добавляем повторный ввод пароля
    password2 = PasswordField('Повторите пароль', validators=[
                              DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})

    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    # Валидатор проверяющий, что такой пользователь существует
    # Вероятно ValidationError понимает, что эту ошибку нужно приписыать
    # к полю username, т.к. ошибка привязывается именно к нему, но
    # в самом поле, в атрибутах, мы этот валидатор к применению не указывали
    def validate_username(self, username):
        # Из формы (см. выше) подтянули username и делаем запрос в базу,
        # сколько у нас таких товарищей, посчитай
        users_count = User.query.filter_by(username=username.data).count()
        # Это у нас форма регистрации, и должно быть 0 предшественников
        # если больше 0, т.е. такое имя есть - то выдаем ошибку
        if users_count > 0:
            raise ValidationError(
                'Пользователь с таким именем уже зарегистрирован')

    # Тоже самое с электронной почтой
    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегистрирован')

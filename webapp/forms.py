from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# Данный класс LoginForm который мы создаем потом трансофрируется в
# html данные, когда мы передадим его в шаблн.

# Добавляем класс в понимании html, т.е. названя разукрашки
# render оказать/отдать={"Разукрашка": "Название разукрашки из getbootstrap"}
class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-primary"})

# ПЕРЕНЕСЛИ все формы из webapp forms в user forms
# webapp forms - удалили, т.к. кроме пользовательских
# форм у нас больше нет

# Функционал "запоминания" пользователя
# Если пользователь авторизуется и закроет браузер,
#  то при следующем входе ему придется делать это снова.
# Научим сайт "запоминать" пользователя.
# Для этого в forms.py добавим поле: BooleanField

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# LoginForm - это наше прозвольное имя экземпляра класса
class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={"class": "form-control"})

    remember_me = BooleanField('Запомнить меня', default=True,
                    render_kw={"class": "form-check-input"})

    # Переменная которая будет транслироваться в hnml форму
    # BooleanField (чек бокс который отдает Правада или Ложь)
    # на странице транслируется как чек-бокс (галочку ставить)
    # Назвали его на странице именем "Запомнить меня"
    # default=True - по умолчанию галочка уже будет стоять
    # render_kw={"class": "form-check-input"}
    #  - разукрашка из БутСтрапа
    # Далее добавляем это поле в шалон логина

    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-primary"})

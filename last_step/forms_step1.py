# Библиотека для работы с формами (шаблонами) во Фласк
# Импортируем класс для работы с формами FlaskForm
# потом от него унаследуемся
from flask_wtf import FlaskForm
# Импортируем типы полей (они тоже классы, от которых унаследуемся)
from wtforms import StringField, PasswordField, SubmitField
# Импортируем валидатор (контролер)
#  DataRequired - контролирует, что в форму действительно что-то введено
# Required - пер. "Обязательный, необходимый"
# Чтобы нам вручную не писать кучу проверок
from wtforms.validators import DataRequired


# Создаем класс LoginForm, который унаследуюем от FlaskForm и сделаем
# несколько полей
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    # Переменная=ПолеТекста "т.е. вдино что пишем" (label 'Имя пользователя',
    #  т.е. видимый на странице текст,
    #   валидаторы "т.е. контролеры"=задаем списком[DataRequired()])
    #  (пока только один валидатор, а можно много)
    password = PasswordField('Пароль', validators=[DataRequired()])
    # Переменная=ПолеПароля "т.е. написанное видем ввиде звеждочек или точекы"
    #  (label 'Пароль', т.е. видимый на странице текст,
    #   валидаторы "т.е. контролеры"=задаем списком[DataRequired()])
    #  (пока только один валидатор, а можно много)
    submit = SubmitField('Отправить')
    # Переменная = Кнопка(label 'Отправить'), без валидаторов, это кнопка

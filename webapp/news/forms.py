# Форма добавления комментариев
# Создадим файл forms.py в блюпринте news и добавим форму:

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
# HiddenField - скрытое поле
from wtforms.validators import DataRequired
# DataRequired - проверка, что поле не пустое


class CommentForm(FlaskForm):
    news_id = HiddenField(
        'ID новости',
        validators=[DataRequired()]
    )

    comment_text = StringField(
        'Текст комментария',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )

    submit = SubmitField(
        'Отправить!',
        render_kw={"class": "btn btn-primary"}
    )

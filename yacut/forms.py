from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, URL, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(
            message='Обязательное поле'),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16), Optional(),
            Regexp(
                r'^[a-zA-Z0-9]+$'
            )
        ]
    )
    submit = SubmitField('Создать')

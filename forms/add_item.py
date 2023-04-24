from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class AddItemForm(FlaskForm):
    item = StringField("Товар")
    submit = SubmitField('Создать')

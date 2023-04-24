from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField


class AddForm(FlaskForm):
    item = SelectField("Товар")
    number = IntegerField('Количество')
    submit = SubmitField('Применить')
    plus = SubmitField('+')

    def __init__(self, content):
        super().__init__()
        self.item.choices = content

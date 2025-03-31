from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange

class TimesTableForm(FlaskForm):
    base = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=1000)])
    table_range = IntegerField(default=12, validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Generate')

class ContentsForm(FlaskForm):
    number = HiddenField('Number')
    operation = HiddenField('Operation')

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
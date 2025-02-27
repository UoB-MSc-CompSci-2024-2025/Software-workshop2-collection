from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
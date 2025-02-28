from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, HiddenField, StringField, IntegerRangeField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')


class DynamicMultiplication(FlaskForm):
    textfield = IntegerField('Enter a number (1-1000)',
                             validators=[DataRequired('You are silly because you need a fill this field'),
                                         NumberRange(min=1, max=1000)])
    submit = SubmitField('Submit', validators=[DataRequired()])
























class DynamicMultiplicationInRange(FlaskForm):
    integer_range = IntegerRangeField('IntegerRange',
                                      validators=[DataRequired('You are silly because you need a fill this field'),
                                                  NumberRange(min=1, max=12)])
    submit = SubmitField('Submit', validators=[DataRequired()])

class UploadCsv(FlaskForm):
    file = FileField('Upload CSV file', validators=[FileRequired(), FileAllowed(['csv', 'CSV files only'])])
    submit = SubmitField('Upload', validators=[DataRequired()])

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, SelectField, FileField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, NumberRange

class CalendarForm(FlaskForm):
    # day = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=5)])
    day = SelectField(choices=[(1,'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5,'Friday')],
                      validators=[DataRequired()])
    hour = IntegerField(validators=[DataRequired(), NumberRange(min=9, max=17)])
    item = StringField(validators=[DataRequired()])
    submit = SubmitField('Display Calendar')

class FileUploadCSVForm(FlaskForm):
    file = FileField('Upload a CSV File', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')

class SelectForm(FlaskForm):
    select_row = HiddenField('Select_Row')
    select_col = HiddenField('Select_Col')



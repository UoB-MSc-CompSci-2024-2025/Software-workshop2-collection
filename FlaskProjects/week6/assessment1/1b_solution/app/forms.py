from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, HiddenField, StringField, SelectField, FileField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')


class CalenderDetail(FlaskForm):
    # day = StringField('Day', default='abc', validators=[DataRequired()])
    day = SelectField('Select',
                           choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), ],
                           default=1)
    hour = StringField('Hour', default='', validators=[DataRequired()])
    item = StringField('Item', default='', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


class UploadCsv(FlaskForm):
    file = FileField('Upload CSV file', validators=[FileRequired(), FileAllowed(['csv', 'CSV files only'])])
    submit = SubmitField('Upload', validators=[DataRequired()])
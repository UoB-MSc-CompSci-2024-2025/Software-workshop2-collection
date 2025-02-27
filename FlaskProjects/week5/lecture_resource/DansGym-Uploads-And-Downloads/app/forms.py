from flask_wtf import FlaskForm

from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('You are silly, enter a username')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    level = SelectField('Level', choices=['None', 'Premium Tier', 'Cheap Tier'])
    height = IntegerField('Height', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_height(self, height):
        if height.data > 150:
            raise ValidationError('You are too tall')
        if height.data < 100:
            raise ValidationError('You are too short')

    def validate_level(self, level):
        if level.data == 'None':
            raise ValidationError('You must chose a level')

class CSVUploadForm(FlaskForm):
    file = FileField('Upload', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Submit')

class ItemForm(FlaskForm):
    fruit_choice = HiddenField('fruit_choice')

class DownloadForm(FlaskForm):
    submit = SubmitField('Download')
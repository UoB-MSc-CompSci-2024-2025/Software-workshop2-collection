from datetime import datetime

from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('You are silly because you need a username')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    height = IntegerField('Height', validators=[DataRequired()])
    # dob = DateField('DoB', validators=[DataRequired()], format="%Y %m %d")
    level = SelectField('Level', choices=[('Premium', 'Premium'), ('Cheap', 'Cheap')])
    submit = SubmitField('Submit', validators=[DataRequired()])

    def validate_height(self, height):
        if height.data > 1000:
            raise ValidationError('You are too tall, we only accept short people')

    def validate_dob(self, dob):
        if dob.data < datetime(2015, 12, 1).date():
            raise ValidationError('You are too old')



class ImageUploadForm(FlaskForm):
    # There should be upload image or file action field
    # There should be a submit button
    image = FileField('Pick your profile picture', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Upload', validators=[DataRequired()])

class CsvUploadForm(FlaskForm):
    csv = FileField('Pick your csv file', validators=[FileRequired(), FileAllowed(['csv', 'CSV files only!'])])
    submit =  SubmitField('Upload', validators=[DataRequired()])


class DownloadForm(FlaskForm):
    submit = SubmitField('Download')

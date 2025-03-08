from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ChangePasswordForm(FlaskForm):
    oldPassword = StringField('Old password', validators=[DataRequired()])
    newPassword = StringField('New password', validators=[DataRequired()])
    confirmPassword = StringField('Confirm password', validators=[DataRequired(), EqualTo('newPassword')])
    submit = SubmitField('Change password')
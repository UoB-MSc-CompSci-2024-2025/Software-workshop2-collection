from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Email


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

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    secondary_email = StringField('Secondary Email')
    role = SelectField('Role', choices=[(2, 'Normal')], default=2, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = StringField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class EmptyForm(FlaskForm):
    delete = HiddenField('Delete')

class UpdateEmailForm(FlaskForm):
    updateEmail = StringField('Update Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

class AddOrEditAddressFrom(FlaskForm):
    addressTag =StringField('Tag', validators=[DataRequired()])
    address = StringField('Enter Address', validators=[DataRequired()])
    phone = StringField('Enter phone')
    submit = SubmitField('Save')
    edit = HiddenField('Edit', default= '-1')


from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User, Address

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


def password_policy(form, field):
    message = """A password must be at least 8 characters long, and have an
                uppercase and lowercase letter, a digit, and a character which is
                neither a letter or a digit"""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_non_let_dig = False
    for ch in field.data:
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
        flg_non_let_dig = flg_non_let_dig or not ch.isalnum()
    if not (flg_upper and flg_lower and flg_digit and flg_non_let_dig):
        raise ValidationError(message)

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message="Passwords must match")])
    submit = SubmitField('Change_Password')

    @staticmethod
    def validate_password(form, field):
        if not current_user.check_password(field.data):
            raise ValidationError("Incorrect password")


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(form, field):
        q = db.select(User).where(User.username==field.data)
        if db.session.scalar(q):
            raise ValidationError("Username already taken, please choose another")

    @staticmethod
    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError("Email address already taken, please choose another")

class AddressForm(FlaskForm):
    edit = HiddenField(default='-1')
    tag = StringField('Tag', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone')
    submit = SubmitField('Submit')


    # Note that the address field is not required to be unique and the phone is optional and not required to be unique
    # but the tag has to be unique among addresses of the same user.
    @staticmethod
    def validate_tag(form, field):
        q = db.select(Address).where(Address.tag==field.data, Address.user==current_user)
        addr = db.session.scalar(q)
        if addr and addr.id != int(form.edit.data):
            raise ValidationError("You already have an address with this tag, please choose another")

class ReviewForm(FlaskForm):
    edit = HiddenField(default='')
    stars = SelectField(choices=[(-1,''),(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], default=-1,
                        validators=[DataRequired()])
    text = TextAreaField('Review Text', validators=[Optional(), Length(max=1024)] )
    submit = SubmitField('Add Review')
    update = SubmitField('Update Review')

    @staticmethod
    def validate_stars(form, field):
        if not (0 <= int(field.data) <= 5):
            raise ValidationError("You must choose a number of stars")

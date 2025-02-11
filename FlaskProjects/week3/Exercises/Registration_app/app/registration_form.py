from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Regexp


# import phonenumbers

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match', )])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])
    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number (10-15 digits, optional '+').")
        ]
    )
    address = StringField('Address', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])

    submit = SubmitField('Register')

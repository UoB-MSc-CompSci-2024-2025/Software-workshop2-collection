from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Regexp, Email, ValidationError
from datetime import date, timedelta


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    date_of_birth = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])
    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number (10-15 digits, optional '+').")
        ]
    )
    address = StringField('Address', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired(), NumberRange(min=100, max=300)])
    weight = FloatField('Weight', validators=[DataRequired(), NumberRange(min=50, max=300)])
    # height = IntegerField('Height', validators=[DataRequired()])
    # weight = IntegerField('Weight',validators=[DataRequired()])
    # email = EmailField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Register')

    def validate_date_of_birth(form, field):
        today = date.today()
        if field.data > today:
            raise ValidationError("Date of birth cannot be in the future.")
        min_age_date = today - timedelta(days=18 * 365)  # Approximate 18 years
        if field.data > min_age_date:
            raise ValidationError("You must be at least 18 years old.")
            # raise ValidationError("Date of birth cannot be in the future.")

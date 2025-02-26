from flask_wtf import FlaskForm
from wtforms import HiddenField

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    choice_two = HiddenField('SecondaryChoice')

    # We don't need a SubmitField because that won't let us use an icon for the button
    # Instead we just put a HTML button element with type="submit", and the icon in the
    # body of the element. That is all we need to submit the form. Note that we don't care
    # what the value or name of the button is.

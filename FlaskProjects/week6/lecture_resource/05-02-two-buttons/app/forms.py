from flask_wtf import FlaskForm
from wtforms import HiddenField


class ChooseForm(FlaskForm):
    choice1_row = HiddenField('Choice1')
    choice2_row = HiddenField('Choice2')
    # We don't need a SubmitField because that won't let us use an icon for the button
    # Instead we just put a HTML button element with type="submit", and the icon in the
    # body of the element. That is all we need to submit the form. Note that we don't care
    # what the value or name of the button is.

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import HiddenField, FileField, SubmitField


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    # We don't need a SubmitField because that won't let us use an icon for the button
    # Instead we just put a HTML button element with type="submit", and the icon in the
    # body of the element. That is all we need to submit the form. Note that we don't care
    # what the value or name of the button is.

class FileUploadTXTForm(FlaskForm):
    file = FileField('Upload a Text File', validators=[FileRequired(), FileAllowed(['txt'])])
    submit = SubmitField('Upload')

class FileUploadCSVForm(FlaskForm):
    file = FileField('Upload a CSV File', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')

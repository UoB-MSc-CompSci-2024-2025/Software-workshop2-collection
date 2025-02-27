# ./week_five/ex_three/app/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, HiddenField, RadioField


class ChooseFrom(FlaskForm):
    starter = SelectField('Starters', choices=[], default=1)
    main = SelectField('Mains', choices=[], default=1)
    dessert = SelectField('Desserts', choices=[], default=1)
    submit = SubmitField('Order')


class RadioForm(FlaskForm):
    starter = RadioField(choices=[])
    main = RadioField(choices=[])
    dessert = RadioField(choices=[])
    submit = SubmitField('Order')


class OptionForm(FlaskForm):
    toggle_view = HiddenField()
    amount = SelectField('Amount', choices=[], default=5)
    choose = StringField('Custom Amount', default='10%')
    submit = SubmitField('Add Service Charge')


class DownloadForm(FlaskForm):
    download_receipt = HiddenField('Receipt')
    download_menu = HiddenField('Menu')

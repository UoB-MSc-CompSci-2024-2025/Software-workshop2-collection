from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField,
                     DateTimeField, DateTimeLocalField, DecimalField,
                     EmailField, FileField, MultipleFileField, FloatField,
                     IntegerRangeField, MonthField, RadioField, SelectField,
                     SearchField, SelectMultipleField, SubmitField, StringField,
                     TelField, TimeField, URLField, PasswordField, TextAreaField,
                     ColorField, FieldList, DecimalRangeField
                     )
from wtforms.validators import NumberRange, Email, DataRequired
import datetime
import decimal

class AllFieldsForm(FlaskForm):
    boolean_f = BooleanField('Boolean', default=True)
    date_f = DateField('Date (DD/MM/YYYY)', default=datetime.date(2025,1,30))
    datetime_f = DateTimeField('DateTime (YYYY-MM-DD HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime.today())
    datetimelocal_f = DateTimeLocalField('DateTimeLocal (format is local: DD/MM/YYYY, HH:MM)', default=datetime.datetime.today())
    decimal_f = DecimalField('Decimal', default=decimal.Decimal(2.71828), places=4)
    decimalrange_f = DecimalRangeField('DecimalRange', default=decimal.Decimal(0.2), validators=[NumberRange(min=0, max=1.5)])
    email_f = EmailField('Email', default='a@b.com', validators=[Email()])
    file_f = FileField('File')
    multiplefile_f = MultipleFileField('MultipleFile')
    float_f = FloatField('Float', default=3.14159)
    integerrange_f = IntegerRangeField('IntegerRange', default=9, validators=[NumberRange(min=0, max=10)])
    month_f = MonthField('Month YYYY-MM', default=datetime.datetime.today())
    radio_f = RadioField('Radio', choices = [(1, 'a'), (2, 'b'), (3,'c')], default=2)
    select_f = SelectField('Select', choices = [(1, 'a'), (2, 'b'), (3,'c')], default=2)
    search_f = SearchField('Search', default='Any search string')
    selectmultiple_f = SelectMultipleField('SelectMultiple', choices = [(1, 'a'), (2, 'b'), (3,'c')], default=[1,3])
    string_f = StringField('String', default='abc')
    tel_f = TelField('Tel', default='any string allowed: use a Regexp validator if you want to restrict')
    time_f = TimeField('Time (HH:MM)', default=datetime.time(hour=15, minute=30))
    url_f = URLField('URL', default='http://127.0.0.1:5000/')
    password_f = PasswordField('Password')
    textarea_f = TextAreaField('TextArea', default='Multiline text\ninput field')
    color_f = ColorField('Color', default='#0000ff')
    fieldlist_f1 = FieldList(StringField('FieldList1'), min_entries=3, default=['a', 'b', 'c'])
    fieldlist_f2 = FieldList(StringField('FieldList2'), min_entries=3, default=['a', 'b', 'c'])
    submit_f = SubmitField('Submit')



class DynamicMultiplication(FlaskForm):
    textfield = StringField('Username', validators=[DataRequired('You are silly because you need a fill this field')])
    submit = SubmitField('Submit', validators=[DataRequired()])

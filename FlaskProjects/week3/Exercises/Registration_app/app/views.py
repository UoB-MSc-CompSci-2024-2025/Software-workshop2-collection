from flask import render_template, url_for
from wtforms.validators import email

from app import app
from app.registration_form import RegistrationForm


@app.route("/")
def home():
    return render_template('home.html', name='Alan', email= '')

@app.route('/mylist')
def mylist():
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst)

@app.route('/registration',  methods=['GET', 'POST'])
def new_user_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return render_template('home.html', name=form.username.data, email=form.email.data )
    return  render_template('registration.html', title='Registration', form = form )

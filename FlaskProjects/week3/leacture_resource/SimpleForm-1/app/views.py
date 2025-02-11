from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route("/")
def home():
    return render_template('home.html', name='Alan', title="Home")

@app.route('/mylist')
def mylist():
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst, title="MyList")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import LoginForm, RegistrationForm

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
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('loginBS2.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # We don't need the flash message as we are sending the user to a
        # Confirmation page
        # flash(f'Registration for {form.username.data}')
        return render_template('registration_received.html', title="Registration Received", form=form)
    return render_template('registerBS3.html', title='Register', form=form)


# view is like controller - which hold the end points
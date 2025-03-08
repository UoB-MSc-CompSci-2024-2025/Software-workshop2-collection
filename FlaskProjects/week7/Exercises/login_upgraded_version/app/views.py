from crypt import methods

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from wtforms.validators import email

from app import app
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
import csv
import io
import re


@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar_one()

            if not_valid_password(form.confirmPassword.data):
                return redirect(url_for('change_password'))

            if not check_password_hash(user.password_hash, form.oldPassword.data):
                flash('Incorrect current password', 'danger')
                return redirect(url_for('change_password'))

            user.set_password(form.confirmPassword.data)
            db.session.commit()

            flash('Updated the password', 'success')

            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Something went wrong {e}', 'success')
            return redirect(url_for('change_password'))

    return render_template('change_password.html', title='Change password', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if not_valid_password(form.confirmPassword.data):
                return render_template('register.html', title='Register', form=form)

            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.confirmPassword.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Register successfully, please login', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            flash(f'{e.orig}, please enter new data', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def not_valid_password(password):
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=!]{8,}', password):
        flash('Password should contain at least 8 characters long, at least 1 digit,'
              '1 uppercase letter, 1 lowercase letter and 1 special character',
              'danger')
        return True
    else:
        return False


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403


# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404


@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413


# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500

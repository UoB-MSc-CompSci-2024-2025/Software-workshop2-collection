from crypt import methods
from time import sleep

from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from wtforms.validators import email

from app import app
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, RegistrationForm, EmptyForm, UpdateEmailForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit
import csv
import io
import re
from datetime import datetime


@app.route("/")
def home():
    if not current_user.is_anonymous and current_user.username is not None:
        user = db.session.scalar(
            sa.select(User).where(User.username == current_user.username))
        if user.previous_login is not None:
            flash(f'The last time logged in time was {user.previous_login}', 'info')
    return render_template('home.html', title="Home")


@app.route('/users', methods=['GET', 'POST'])
def users():
    form = EmptyForm()
    users_result = []
    try:
        users_result.append(
            ['Id', 'User Name', 'Email', 'Secondary Email', 'Role', 'Logged in Data/time', 'Switch User role',
             'Delete user'])
        query = db.select(User)
        users_result.extend(db.session.scalars(query).all())
    except Exception as e:
        flash(f'Something went wrong {e}', 'danger')

    return render_template('users.html', title='Users', users=users_result, form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateEmailForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar_one()

        if user.email == form.updateEmail.data:
            flash('User already have this email stored', 'warning')
        else:
            user.email = form.updateEmail.data
            db.session.commit()

            flash('Updated the email', 'success')

        return redirect(url_for('account'))
    return render_template('account.html', title="Account", form=form)


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
        user.previous_login = user.current_login
        user.current_login = str(datetime.now())[:19]
        db.session.commit()

        # if user.previous_login is not None:
        #     flash(f'The last time logged in time was {user.previous_login}', 'info')

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
            flash(f'Something went wrong {e}', 'danger')
            return redirect(url_for('change_password'))

    return render_template('change_password.html', title='Change password', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if not_valid_password(form.confirmPassword.data):
                return render_template('register.html', title='Register', form=form)

            if form.email.data == form.secondary_email.data:
                flash(
                    f'{form.secondary_email.data} secondary should not be the same, please enter new email',
                    'danger')
                return redirect(url_for('register'))

            users = db.session.scalars(db.select(User)).all()

            email_map = {}
            for user in users:
                if user.email not in email_map:
                    email_map[user.email] = 1
                if user.secondary_email is not None and user.secondary_email not in email_map:
                    email_map[user.secondary_email] = 1

                if user.email in email_map:
                    email_map[user.email] += 1
                if user.secondary_email in email_map:
                    email_map[user.secondary_email] += 1

                if form.secondary_email.data in email_map and email_map[form.secondary_email.data] > 1:
                    flash(
                        f'{form.secondary_email.data or form.email.data} is already available, please enter new email',
                        'danger')
                    return redirect(url_for('register'))

            new_user = User(username=form.username.data, email=form.email.data, role=form.role.data[0],
                            secondary_email=form.secondary_email.data)
            new_user.set_password(form.confirmPassword.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Register successfully, please login', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            flash(f'{e.orig}, please enter new data', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.get(User, int(form.delete.data))
        if int(user.role) == 1:
            admins = db.session.scalars(
                db.select(User.id, User.username).where(User.role == 1)).all()
            if len(admins) > 1:
                # delete admin user where we have multiple admin
                db.session.delete(user)
                db.session.commit()
                if user.id == current_user.id:
                    logout_user()
                    return redirect(url_for('login'))
                flash('User deleted!', 'success')

            else:
                flash('You can\'t delete the only admin available', 'danger')
        else:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted!', 'success')

    return redirect(url_for('users'))


@app.route('/toggle_user_role', methods=['GET', 'POST'])
def toggle_user_role():
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.get(User, int(form.delete.data))
        if int(user.role) == 1:
            admins = db.session.scalars(
                db.select(User.id, User.username).where(User.role == 1)).all()
            if len(admins) > 1:
                user.role = 2
                db.session.commit()
                if user.id == current_user.id:
                    logout_user()
                    return redirect(url_for('login'))
                flash('User updated!', 'success')
            else:
                flash('You can\'t update the only admin available', 'danger')
        else:
            user.role = 1
            db.session.commit()
            flash('User updated!', 'success')

    return redirect(url_for('users'))


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

#     <button class="btn" type="submit" onclick="this.form.delete.value='{{ user.id }}'">
#                             <i class="bi bi-toggle-on "></i>
#                         </button>


# <script>
# function submitForm(button, userId) {
#     let form = button.closest('form');
#     form.querySelector("#selected_user").value = userId;
#     form.submit();
# }
# </script>

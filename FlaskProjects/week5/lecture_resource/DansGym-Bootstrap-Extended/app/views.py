from email_validator import validate_email, EmailNotValidError
from flask import render_template, redirect, url_for, request, flash, send_from_directory
from werkzeug.utils import secure_filename

from app import app
from app.forms import RegistrationForm, ImageUploadForm, CSVUploadForm, ItemForm

from uuid import uuid4
import os

import csv

@app.route('/')
def home():
    return render_template('home.html', title='Home Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register.html', form=form)


@app.route('/register2', methods=['GET', 'POST'])
def register2():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register2.html', form=form)


@app.route('/register3', methods=['GET', 'POST'])
def register3():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have registered correctly {form.username.data}', 'success')
        return redirect(url_for('reg_complete', username=form.username.data, email=form.email.data, level=form.level.data))
    return render_template('register3.html', form=form)

@app.route('/register_complete')
def reg_complete():
    username = request.args.get('username')
    email = request.args.get('email')
    level = request.args.get('level')
    return render_template('reg_complete.html', username=username, email=email, level=level)

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    form = ImageUploadForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            flash('File uploaded', 'success')
            return render_template('upload_complete.html', title='Upload complete', user_image=url_for('download_file', name=filename))

    return render_template('upload_image.html', title="Please upload an image", form=form)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    form = CSVUploadForm()
    error_count = 0
    staff = []
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)

            try:
                with open(filepath, newline='') as csvFile:
                    reader = csv.reader(csvFile)
                    header_row = next(reader)
                    if header_row != ['StaffName', 'Email', 'TimeAtCompany']:
                        form.file.errors.append('Your header row is wrong or doesn\'t exist')
                        raise ValueError()
                    for row_num, row in enumerate(reader):
                        if error_count > 5:
                            form.file.errors.append('Your file is crap, so I\'m giving up')
                            raise ValueError
                        if len(row) != 3:
                            form.file.errors.append(f'Row {row_num} is crap because of length')
                            error_count += 1
                            continue
                        if not valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} is crap because of email')
                            error_count += 1
                            continue
                        if error_count == 0:
                            staff.append(row)
                if error_count > 0:
                    raise ValueError

                flash('File uploaded', 'success')
                return render_template('upload_complete_csv.html', title='Upload complete',
                                       user_image=url_for('download_file', name=filename))
            except ValueError:
                flash(f'You did it wrong')
            finally:
                silent_remove(filepath)

    return render_template('upload_image.html', title="Please upload an image", form=form)

def valid_email(email_address):
    try:
        validate_email(email_address)
    except EmailNotValidError:
        return False
    return True

def silent_remove(path):
    try:
        os.remove(path)
    except:
        pass


my_list = ['Lemon', 'Apple', 'Orange']

@app.route('/show_list')
def show_list():
    form = ItemForm()
    return render_template('list.html', my_list=my_list, form=form)


@app.route('/delete', methods=['GET', 'POST'])
def delete_item():
    form = ItemForm()
    if form.validate_on_submit():
        choice = int(form.choice.data)
        if choice > len(my_list):
            flash('ERROR', 'warning')
        else:
            flash('Item deleted', 'danger')
            my_list.pop(choice)
    return redirect(url_for('show_list'))

@app.route('/reset', methods=['GET', 'POST'])
def reset_items():
    form = ItemForm()
    if form.validate_on_submit():
        my_list.clear()
        my_list.extend(['Lemon', 'Apple', 'Orange'])
        flash('Items reset', 'success')
    return redirect(url_for('show_list'))

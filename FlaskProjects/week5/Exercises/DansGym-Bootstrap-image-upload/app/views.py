import os.path
from crypt import methods
from uuid import uuid4

from flask import render_template, url_for, redirect, request, flash, send_from_directory
from werkzeug.utils import secure_filename

from app import app
from app.forms import RegistrationForm, ImageUploadForm


@app.route('/')
def home():
    return render_template('home.html', title='Home Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have successfully created an account for username: {form.username.data}', 'success')
        return redirect(url_for('registration_confirmed', username=form.username.data, email=form.email.data,
                                level=form.level.data))
    return render_template('register.html', title='Register', form=form)


@app.route('/register2', methods=['GET', 'POST'])
def register2():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have successfully created an account for username: {form.username.data}', 'success')
        return redirect(url_for('registration_confirmed', username=form.username.data, email=form.email.data,
                                level=form.level.data))
    return render_template('register2.html', title='Register2', form=form)


@app.route('/register3', methods=['GET', 'POST'])
def register3():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'You have successfully created an account for username: {form.username.data}', 'success')
        return redirect(url_for('registration_confirmed', username=form.username.data, email=form.email.data,
                                level=form.level.data))
    return render_template('register3.html', title='Register3', form=form)


@app.route('/reg_confirmed')
def registration_confirmed():
    username = request.args.get('username')
    email = request.args.get('email')
    level = request.args.get('level')
    return render_template('reg_confirmed.html', username=username, email=email, level=level)


@app.route('/upload_image', methods = ['GET','POST'])
def upload_image():
    form = ImageUploadForm()
    if form.validate_on_submit():
        if form.image.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.image.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            flash('File uploaded', 'success')
            return render_template('upload_complete.html', title='Upload_complete', user_image=url_for('view_user_image', name=filename))
    return render_template('upload_image.html',title ="Please upload an image", form=form)



@app.route('/uploads/<name>')
def view_user_image(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

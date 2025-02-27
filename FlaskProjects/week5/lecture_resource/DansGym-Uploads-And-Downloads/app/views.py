import io

from flask import render_template, redirect, url_for, request, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename

from app import app
from app.forms import RegistrationForm, CSVUploadForm, ItemForm, DownloadForm
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

fruit = [['Banana', 'Yellow'], ['Apple', 'Red']]
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    form = CSVUploadForm()
    if form.validate_on_submit():
        unique_str = str(uuid4())
        filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        try:
            with open(filepath, newline='') as csvFile:
                reader = csv.reader(csvFile)
                header_row = next(reader)
                if header_row != ['FruitName', 'Colour']:
                    form.file.errors.append('Your header row is wrong')
                    raise ValueError('The header row is wrong')
                error_count = 0
                temp_fruit = []
                for index, row in enumerate(reader, start=2):
                    if error_count >= 3:
                        raise ValueError('Checking stopped: Too many errors in file')
                    if len(row) != 2:
                        form.file.errors.append(f'Row {index} has the wrong number of fields')
                        error_count += 1
                        continue
                    if row[1] not in ['Red', 'Orange', 'Yellow']:
                        form.file.errors.append(f'Row {index} has an invalid colour')
                        error_count += 1
                        continue
                    temp_fruit.append(row)
                if error_count == 0:
                    fruit.extend(temp_fruit)
                else:
                    raise ValueError('Errors found: file not uploaded')
            return render_template('upload_complete.html', fruit=fruit)
        except ValueError as e:
            flash(e, 'danger')
            print(f"There was an error: {e}")
        finally:
            silent_remove(filepath)
    return render_template('upload_csv.html', form=form)

def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass

@app.route('/show_list')
def show_list():
    form = ItemForm()
    return render_template('list.html', fruit=fruit, form=form)

@app.route('/delete', methods=['POST'])
def delete():
    form = ItemForm()
    if form.validate_on_submit():
        fruit_choice = int(form.fruit_choice.data)
        fruit.pop(fruit_choice)
        flash(f'Item {fruit_choice} deleted', 'warning')
    return redirect(url_for('show_list'))

@app.route('/download')
def download():
    form = DownloadForm()
    if form.validate_on_submit:
        return send_from_directory('static', 'MyFile.csv', as_attachment=True, download_name='MyFile.csv', mimetype='text/csv')
    return render_template('download.html', form=form)

@app.route('/download-dynamic')
def download_dynamic():
    form = DownloadForm()
    if form.validate_on_submit:
        with io.StringIO() as mem:
            writer = csv.writer(mem)
            writer.writerow(['FruitName', 'Colour'])
            for item in fruit:
                writer.writerow(item)
            mem.seek(0)
            return send_file(io.BytesIO(mem.getvalue().encode(encoding='utf-8')), as_attachment=True, download_name='MyFruit.csv', mimetype='text/csv')
    return render_template('download.html', form=form)
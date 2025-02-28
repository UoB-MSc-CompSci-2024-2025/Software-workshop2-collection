import csv
import io
from datetime import datetime
import os.path
from uuid import uuid4

from flask import render_template, url_for, redirect, request, flash, send_from_directory, send_file
from werkzeug.utils import secure_filename

from app import app
from app.forms import RegistrationForm, ImageUploadForm, CsvUploadForm, DownloadForm


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


# Upload Images
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    form = ImageUploadForm()
    if form.validate_on_submit():
        if form.image.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.image.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            flash('File uploaded', 'success')
            return render_template('upload_complete.html', title='Upload_complete',
                                   user_image=url_for('view_user_image', name=filename))
    return render_template('upload_image.html', title="Please upload an image", form=form)


@app.route('/uploads/<name>')
def view_user_image(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


contacts = []
# Upload CSV routes
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    form = CsvUploadForm()
    if form.validate_on_submit():
        if form.csv.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.csv.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.csv.data.save(filepath)

            try:
                with open(filepath) as csvFile:
                    reader = csv.reader(csvFile)
                    header_row = next(reader)
                    if header_row != ['Name', 'Email', 'Phone', 'Birthday']:
                        form.csv.errors.append(
                            'First row of file must be a Header row containing "Name, Email, Phone, Birthday')
                        raise ValueError()
                    header_row.append('Age')
                    contacts.append(header_row)
                    name_duplicate = {}
                    has_duplicate = False

                    for idx, row in enumerate(reader):
                        if row[3] is not None and not is_valid_date(row[3]):
                            form.csv.errors.append(
                                f'The date formate is not correct for this user {row[idx]}')
                            raise ValueError()
                        elif row[3] is not None and is_valid_date(row[3]):
                            if not is_valid_date_range(row[3]):
                                form.csv.errors.append(f'The date is not in the expected range for user {row[idx]}')
                                raise ValueError()

                        if row[0] is not None:
                            if row[0] in name_duplicate:
                                name_duplicate[row[0]] = name_duplicate[row[0]] + 1
                            else:
                                converted_date = datetime.strptime(row[3], "%d/%m/%Y")
                                row.append(f'{datetime.now().year - converted_date.year}')
                                contacts.append(row)
                                name_duplicate[row[0]] = 1

                        if row[0] is not None and name_duplicate[row[0]] >= 2:
                            has_duplicate = True

                    if has_duplicate:
                        flash(f'File Uploaded and duplicate users were removed', 'success')
                        # form.csv.errors.append(f'The file has duplicate name, please remove it!')
                        # raise ValueError
                    else:
                        flash(f'File Uploaded', 'success')

                    return render_template('upload_csv_complete.html', title='Upload csv complete', contacts=contacts)
            except ValueError as error:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
            finally:
                silent_remove(filepath)

    return render_template('upload_csv.html', title='Please upload a csv', form=form)


@app.route('/download')
def download():
    form = DownloadForm()
    if form.validate_on_submit:
        return send_from_directory('static', 'MyFile.csv', as_attachment=True, download_name="MyFile.csv",
                                   mimetype="text/csv")
    return render_template('download.html', form=form)


@app.route('/dynamic_download')
def dynamic_download():
    form = DownloadForm()
    if form.validate_on_submit:
        with io.StringIO() as mem:
            writer = csv.writer(mem)
            for item in contacts:
                item.pop()
                writer.writerow(item)
            mem.seek(0)
            return send_file(io.BytesIO(mem.getvalue().encode(encoding='utf-8')), as_attachment=True,
                                   download_name="MyFruitFile.csv", mimetype="text/csv")
    return render_template('download.html', form= form)


def is_valid_date(date):
    try:
        return datetime.strptime(date, "%d/%m/%Y")
    except ValueError as error:
        return False


def is_valid_date_range(date):
    converted_date = datetime.strptime(date, "%d/%m/%Y")
    return datetime.now().date() >= converted_date.date() > datetime(1905, 2, 25).date()


def silent_remove(filepath):
    try:
        os.remove(filepath)
    except Exception as e:
        pass
    return

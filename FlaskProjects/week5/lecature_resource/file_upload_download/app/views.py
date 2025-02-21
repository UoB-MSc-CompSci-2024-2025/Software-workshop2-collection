from flask import render_template, flash,  url_for, redirect, send_file, send_from_directory
from app import app
from app.forms import ChooseForm, FileUploadTXTForm, FileUploadCSVForm
from email_validator import validate_email, EmailNotValidError
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import csv
import datetime
import io

# Utility function to check if an email string is valid
def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


# Utility function to attempt to remove a file but silently cancel any exceptions if anything goes wrong
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


@app.route("/")
def home():
    app.logger.debug("Debug")
    app.logger.info("Info")
    app.logger.warning("Warning")
    app.logger.error("Error")
    app.logger.critical("Critical")
    return render_template('home.html', name='Alan', title="Home")


@app.route('/upload_txt_file', methods=['GET', 'POST'])
def upload_txt_file():
    lines = []
    form = FileUploadTXTForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            try:
                with open(filepath, newline='') as txtFile:
                    for line in txtFile:
                        lines.append(line)
                flash(f'File Uploaded', 'success')
                return render_template('display_text.html', title='Display Text', lines=lines)
            except Exception as err:
                flash(f'File upload failed.'
                      ' please try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload_file.html', title='Upload Text File', form=form)


@app.route('/upload_csv_file', methods=['GET', 'POST'])
def upload_csv_file():
    lines = []
    contacts = []
    form = FileUploadCSVForm()
    if form.validate_on_submit():
        if form.file.data:
            unique_str = str(uuid4())
            filename = secure_filename(f'{unique_str}-{form.file.data.filename}')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            try:
                with open(filepath, newline='') as csvFile:
                    reader = csv.reader(csvFile)
                    error_count = 0
                    header_row = next(reader)
                    if header_row != ['Name', 'Email', 'Phone']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Name,Email,Phone"')
                        raise ValueError()
                    contacts.append(header_row)
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 3:
                            form.file.errors.append(f'Row {row_num} does not have precisely 3 fields')
                            error_count += 1
                            continue
                        if not is_valid_email(row[1]):
                            form.file.errors.append(f'Row {row_num} has an invalid email: "{row[1]}"')
                        if error_count == 0:
                            contacts.append(row)
                if error_count > 0:
                    raise ValueError
                flash(f'File Uploaded', 'success')
                return render_template('display_contacts.html', title='Display Contacts', contacts=contacts)
            except Exception as err:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload_file.html', title='Upload CSV File', form=form)

@app.route('/download_file', methods=['GET', 'POST'])
def download_file():
    form=ChooseForm()
    if form.validate_on_submit():
        chosen = form.choice.data
        try:
            if chosen == 'Static':
                return send_from_directory('static', 'phonebook.xlsx', as_attachment=True, download_name='sample.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            elif chosen == 'Dynamic':
                text = f'This is a text file dynamically generated on {datetime.datetime.now()}'
                mem = io.BytesIO()
                mem.write(text.encode(encoding="utf-8"))
                mem.seek(0)
                return send_file(mem, as_attachment=True, download_name='output.txt', mimetype='text/plain')
        except Exception as err:
            flash(f'File Download failed.'
                  ' please try again', 'danger')
            app.logger.error(f'Exception occurred in File Download: {err=}')
    return render_template('download.html', title='Download', form=form)



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
    return (render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500))
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
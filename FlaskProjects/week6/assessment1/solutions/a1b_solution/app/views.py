from flask import render_template, redirect, url_for, flash, send_file, send_from_directory
from app import app
from app.forms import CalendarForm, FileUploadCSVForm, SelectForm
from uuid import uuid4
from werkzeug.utils import secure_filename
import csv
import io
import os

@app.route("/")
def home():
    return render_template('home.html', title="Home")

def gen_calendar(lst_slots):
    cal = [['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
    for hour in range(9,18):
        cal.append( [f'{hour:02}:00', '', '', '', '', ''])
    for slot in lst_slots:
        day_idx, hour_idx, item = slot
        hour_idx = hour_idx -8 # starts at 9 but +1 for header row
        cal[hour_idx][day_idx] = item
    return cal

@app.route("/timeslot/<day>/<hour>/<item>")
def timeslot(day, hour, item):
    if not day in ['1', '2', '3', '4', '5']:
        flash(f'Error: Day must be a number between 1 and 5 for Monday to Friday. You entered: "{day}"', 'danger')
        return redirect(url_for('home'))
    if (not hour.isdigit()) or len(hour) > 2 or int(hour) < 9 or int(hour) > 17:
        flash(f'Error: Hour must be a number between 9 and 17 for time slots 09:00 to 17:00. You entered: "{hour}"', 'danger')
        return redirect(url_for('home'))

    slot = (int(day), int(hour), item)
    cal = gen_calendar([slot])
    return render_template('calendar.html', title="Calendar", cal=cal)

@app.route("/display_calendar", methods=['GET', 'POST'])
def display_calendar():
    form = CalendarForm()
    if form.validate_on_submit():
        slot = (int(form.day.data), int(form.hour.data), form.item.data)
        cal = gen_calendar([slot])
        return render_template('calendar.html', title="Calendar", cal=cal)
    return render_template('generic_form.html', title="Display Calendar", form=form)

# Utility function to attempt to remove a file but silently cancel any exceptions if anything goes wrong
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except Exception as err:
        app.logger.warning(f'Error in trying to delete uploaded file: {err=}')
    return

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
                slot_set = set()
                slot_list = []
                with open(filepath, newline='') as csvFile:
                    reader = csv.reader(csvFile)
                    error_count = 0
                    header_row = next(reader)
                    if header_row != ['Day', 'Hour', 'Item']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Day,Hour,Item"')
                        raise ValueError()
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header

                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) == 0:
                            continue
                        if len(row) != len(header_row):
                            form.file.errors.append(f'Row {row_num} does not have precisely {len(header_row)} fields')
                            error_count += 1
                            continue
                        if not row[0] in ['1', '2', '3', '4', '5']:
                            form.file.errors.append(f'Row {row_num} has an invalid day value: "{row[0]}". '
                                                    f'It must be between 1 and 5 for Monday to Friday')
                            error_count += 1
                            continue
                        day = int(row[0])
                        if (not row[1].isdigit()) or len(row[1]) > 2 or int(row[1]) < 9 or int(row[1]) > 17:
                            form.file.errors.append(f'Row {row_num} has an invalid hour value: "{row[1]}". '
                                  f'It must be a number between 9 and 17 for time slots 09:00 to 17:00.')
                            error_count += 1
                            continue
                        hour = int(row[1])
                        if len(row[2]) == 0:
                            form.file.errors.append(f'Row {row_num} has an invalid item value. It must be a non empty string.')
                            error_count += 1
                            continue
                        item = row[2]
                        if (day, hour) in slot_set:
                            form.file.errors.append(f'Row {row_num} has an slot with the same day and hour as a previous one in'
                                  f'the CSV file.')
                            error_count += 1
                            continue
                        slot_set.add((day,hour))
                        if error_count == 0:
                            slot_list.append((day, hour, item))
                if error_count > 0:
                    raise ValueError(f'{error_count=}')
                flash(f'File Uploaded', 'success')
                cal = gen_calendar(slot_list)
                return render_template('calendar.html', title="Calendar", cal=cal)
            except ValueError as err:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
                app.logger.error(f'ValueError occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload_file.html', title='Upload CSV File', form=form)


@app.route("/select", methods=['GET', 'POST'])
def select():
    selected = (-1,-1)
    cal = gen_calendar([])
    form = SelectForm()
    if form.validate_on_submit():
        selected = (int(form.select_row.data), int(form.select_col.data))
    return render_template('select.html', title='Select', form=form, cal=cal, selected=selected)


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
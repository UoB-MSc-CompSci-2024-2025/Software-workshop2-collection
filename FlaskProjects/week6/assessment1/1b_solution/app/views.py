import os
from uuid import uuid4

from flask import render_template, redirect, url_for, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename

from app import app
from app.forms import ChooseForm, CalenderDetail, UploadCsv
import csv
import io

timetable = []


@app.route("/")
def home():
    timetable.clear()
    gen_calender()
    return render_template('home.html', title="Home")


@app.route("/timeslot/<day>/<hour>/<item>")
def timeslot(day, hour, item):
    if not day and not hour and not item:
        return "Invalid request", 400
    if 5 >= int(day) >= 1 and 17 >= int(hour) >= 7:
        schedule = update_calender(day, hour, item)
    else:
        flash(f'Given date is not appropriate, Try again', 'danger')
        return render_template('home.html', title="Home")

    return render_template('calender.html', title=f'Time table', timetable=schedule)


@app.route('/display_calender', methods=['GET', 'POST'])
def display_calender():
    form = CalenderDetail()

    if form.validate_on_submit():
        day = form.day.data[0]
        item = form.item.data
        hour = form.hour.data
        return redirect(url_for('timeslot', day=day, hour=hour, item=item))

    return render_template('calender_details.html', title='Calender Details', form=form)


@app.route('/upload_slots', methods=['GET', 'POST'])
def upload_slots():
    table = []
    form = UploadCsv()
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
                    if header_row != ['Day', 'Hour', 'Item']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Day, Hour, Item"')
                        raise ValueError()
                    table.append(header_row)
                    duplicates = {}
                    for idx, row in enumerate(reader):
                        row_num = idx + 2
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 3:
                            form.file.errors.append(f'Row {row_num} does not have precisely 3 fields')
                            error_count += 1
                            continue
                        for e in row:
                            if not e:
                                form.file.errors.append(f'Row {row_num} has empty string')
                                error_count += 1
                                continue

                        if row[0] is not None:
                            if f'{row[0]}_{row[1]}' in duplicates:
                                duplicates[f'{row[0]}_{row[1]}'] = duplicates[f'{row[0]}_{row[1]}'] + 1
                            else:
                                duplicates[f'{row[0]}_{row[1]}'] = 1

                        if row[0] is not None and duplicates[f'{row[0]}_{row[1]}'] >= 2:
                            form.file.errors.append(f'Row {row_num} has duplicate')
                            error_count += 1
                            continue

                        if error_count == 0:
                            table.append(row)
                if error_count > 0:
                    raise ValueError
                flash(f'File Uploaded', 'success')
                timetable.clear()
                gen_calender()
                temp = table[1:]
                for i, row in enumerate(temp):
                    update_calender(row[0], row[1], row[2])
                return redirect(url_for('timeslot', day=table[-1][0], hour=table[-1][1], item=table[-1][2]))
            except Exception as err:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload.html', title='Upload Table', form=form)


@app.route("/select")
def select():
    timetable.clear()
    schedule = gen_calender()
    return render_template('calender.html', title=f'Time table', timetable=schedule)


def gen_calender():
    timetable.append(['Timings', "Monday", "Tuesday", "Wednesday", 'Thursday', 'Friday'])
    index = 1
    for i in range(9, 18):
        timetable.append([i, '', '', '', '', ''])
        index += 1
    return timetable


def update_calender(day, hour, item):
    temp = timetable[1:]
    for i, row in enumerate(temp, 2):
        if int(row[0]) == int(hour):
            row[int(day)] = item
    return timetable


def silent_remove(filepath):
    try:
        os.remove(filepath)
    except Exception as e:
        pass
    return


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

import os
from uuid import uuid4

from flask import (render_template, send_file, request, flash)
from werkzeug.utils import secure_filename

from app import app

import csv
import io

from app.forms import DynamicMultiplication, ChooseForm, UploadCsv


@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/table/<number>")
def table_3(number):
    form = DynamicMultiplication()
    if not number:
        return "Invalid request", 400

    multiples = get_multiples(int(number))
    return render_template('table3.html', title=f'Table {number}', multiples=multiples, form=form)


@app.route('/table', methods=['GET', 'POST'])
def table():
    form = DynamicMultiplication()
    multiples = None

    if form.validate_on_submit():
        number = form.textfield.data
        multiples = get_multiples(number)

    return render_template('table.html', title='Tables', form=form, multiples=multiples)


@app.route('/table_range_multiples', methods=['GET', 'POST'])
def table_range_multiples():
    form = ChooseForm()
    number = request.form.get('number')
    if not number:
        return "Invalid request", 400

    multiples = get_multiples(int(number))

    return render_template('tables_from_range.html', title='Tables Range', form=form, multiples=multiples)


@app.route('/table_range', methods=['GET', 'POST'])
def table_range():
    form = ChooseForm()
    return render_template('table_range.html', title='Table Range', form=form, range=12)


@app.route('/download', methods=['POST'])
def download():
    number = request.form.get('number')
    if not number:
        return "Invalid request", 400

    multiples = get_multiples(int(number))

    # Create CSV in memory
    mem = io.StringIO()
    writer = csv.writer(mem)
    writer.writerows(multiples)
    mem.seek(0)

    return send_file(
        io.BytesIO(mem.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=f"Multiplication_Table_{number}.csv",
        mimetype="text/csv"
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload():
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
                    name_duplicate = {}
                    has_duplicate = False
                    if header_row != ['Multiplicand', 'Multiplier', 'Product']:
                        form.file.errors.append(
                            'First row of file must be a Header row containing "Multiplicand, Multiplier, Product"')
                        raise ValueError()
                    table.append(header_row)
                    for idx, row in enumerate(reader):
                        row_num = idx + 2  # Spreadsheets have the first row as 0, and we skip the header
                        if error_count > 10:
                            form.file.errors.append('Too many errors found, any further errors omitted')
                            raise ValueError()
                        if len(row) != 3:
                            form.file.errors.append(f'Row {row_num} does not have precisely 3 fields')
                            error_count += 1
                            continue

                        
                        if error_count == 0:
                            table.append(row)
                if error_count > 0:
                    raise ValueError
                flash(f'File Uploaded', 'success')
                return render_template('table3.html', title='Display Uploaded table', multiples=table, form=form)
            except Exception as err:
                flash(f'File upload failed.'
                      ' Please correct your file and try again', 'danger')
                app.logger.error(f'Exception occurred: {err=}')
            finally:
                silent_remove(filepath)
    return render_template('upload.html', title='Upload Table', form=form)


# Function to Generate Multiplication Table
def get_multiples(multiplicand):
    products = [["Multiplicand", "Multiplier", "Product"]]
    for i in range(1, 11):
        products.append([multiplicand, i, multiplicand * i])
    return products

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

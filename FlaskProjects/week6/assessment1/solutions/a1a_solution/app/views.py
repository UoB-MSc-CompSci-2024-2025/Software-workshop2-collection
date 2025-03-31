from flask import render_template, redirect, url_for, flash, send_file, send_from_directory
from app import app
from app.forms import TimesTableForm, ContentsForm, ChooseForm
import csv
import io

@app.route("/")
def home():
    return render_template('home.html', title="Home")

@app.route("/times/<num>")
def times(num):
    if (not num.isdigit()) or len(num) > 4 or int(num) < 1 or int(num) > 1000:
        flash(f'Error: Times Table request needs a number between 1 and 1000')
        return redirect(url_for('home'))
    base = int(num)
    times_table = [(base, i, base*i) for i in range(1,13)]
    return render_template('times_table.html', title="Times " + str(base), base=base, times_table=times_table)

@app.route("/display_times", methods=['GET', 'POST'])
def display_times():
    form = TimesTableForm()
    if form.validate_on_submit():
        base = form.base.data
        table_range = form.table_range.data
        times_table = [(base, i, base*i) for i in range(1,table_range+1)]
        return render_template('times_table.html', title="Times " + str(base), base=base, times_table=times_table)
    return render_template('generic_form.html', title="Generate Times Table", form=form)

@app.route("/download_times", methods=['GET', 'POST'])
def download_times():
    form = TimesTableForm()
    if form.validate_on_submit():
        base = form.base.data
        table_range = form.table_range.data
        times_table = [('Base', 'Multiplier', 'Product')] + [(base, i, base*i) for i in range(1,table_range+1)]
        mem_str = io.StringIO()
        csv_writer = csv.writer(mem_str)
        csv_writer.writerows(times_table)

        mem_bytes = io.BytesIO()
        mem_bytes.write(mem_str.getvalue().encode(encoding="utf-8"))
        mem_bytes.seek(0)
        return send_file(mem_bytes, as_attachment=True, download_name=str(base) + '_times_table.csv', mimetype='text/csv')
    return render_template('generic_form.html', title="Download Times Table", form=form)

@app.route("/contents")
def contents():
    form=ContentsForm()
    return render_template('contents.html', title="Contents", form=form)

@app.route('/contents_op', methods=['POST'])
def contents_op():
    form=ContentsForm()
    if form.validate_on_submit():
        base = int(form.number.data)
        op = form.operation.data
        times_table = [(base, i, base * i) for i in range(1, 13)]
        if op == 'Display':
            return render_template('times_table.html', title="Times " + str(base), base=base, times_table=times_table)
        elif op == 'Download':
            mem_str = io.StringIO()
            csv_writer = csv.writer(mem_str)
            csv_writer.writerows(times_table)

            mem_bytes = io.BytesIO()
            mem_bytes.write(mem_str.getvalue().encode(encoding="utf-8"))
            mem_bytes.seek(0)
            return send_file(mem_bytes, as_attachment=True, download_name=str(base) + '_times_table.csv',
                             mimetype='text/csv')
        else:
            app.logger.error(f'Unknown operation requested from contents_op: {op}')
            flash(f'Internal Error', 'danger')
    return redirect(url_for('home'))



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
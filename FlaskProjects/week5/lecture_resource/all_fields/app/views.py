from flask import render_template, flash, request
from app import app
from app.forms import AllFieldsForm, DynamicMultiplication


@app.route("/")
def home():
    return render_template('home.html', name='Alan', title="Home")

@app.route('/all_fields_quick_form', methods=['GET', 'POST'])
def all_fields_quick_form():
    form = AllFieldsForm()
    if form.validate_on_submit():
        return render_template('all_fields_quick_form.html', title='QF All Fields', form=form)
    return render_template('all_fields_quick_form.html', title='QF All Fields', form=form)

@app.route('/all_fields_manual', methods=['GET', 'POST'])
def all_fields_manual():
    form = AllFieldsForm()
    if form.validate_on_submit():
        flash('Submit successful', 'success')
        return render_template('all_fields_manual.html', title='Man All Fields', form=form)
    elif request.method == 'POST':
        flash('Submit failed', 'danger')
    return render_template('all_fields_manual.html', title='Man All Fields', form=form)


@app.route('/table', methods=['GET', 'POST'])
def table():
    form = DynamicMultiplication()
    if form.validate_on_submit():
        return render_template('table.html', title='QF All Fields', form=form)
    return render_template('table.html', title='QF All Fields', form=form)
from flask import render_template, flash
from app import app
from app.forms import ChooseForm

@app.route("/")
def home():
    return render_template('home.html', name='Alan', title="Home")

@app.route('/mylist')
def mylist():
    form=ChooseForm()
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst, title="MyList", form=form, chosen=-1)


@app.route('/choose', methods=['POST'])
def choose():
    lst = ['Car', 'House', 'TV']
    form = ChooseForm()
    if form.validate_on_submit():
        chosen = int(form.choice.data)
        if chosen != -1:
            flash(f'{lst[chosen]} chosen', 'success')
        else:
            flash('None chosen', 'success')
        return render_template('list.html', lst=lst, title='ChoiceList', form=form, chosen=chosen)
    return render_template('list.html', lst=lst, title='ChoiceList', form=form, chosen=-1)

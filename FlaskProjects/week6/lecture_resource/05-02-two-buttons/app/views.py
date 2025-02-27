from flask import render_template, flash
from app import app
from app.forms import ChooseForm

@app.route("/")
def home():
    return render_template('home.html', name='Alan', title="Home")


@app.route('/mylist')
def mylist():
    lst = ['Car', 'House', 'TV', 'Laptop', 'Armchair']
    form=ChooseForm()

    return render_template('list.html', lst=lst, title="MyList", form=form, chosen1=-1, chosen2=-1)


@app.route('/choose', methods=['POST'])
def choose():
    lst = ['Car', 'House', 'TV', 'Laptop', 'Armchair']
    chosen1 = chosen2 = -1
    form = ChooseForm()
    if form.validate_on_submit():
        chosen1 = int(form.choice1_row.data)
        chosen2 = int(form.choice2_row.data)
        if (chosen1 != -1) and (chosen1 == chosen2):
            form.choice2_row.errors.append(f'You can not choose the same item as your primary and secondary choice')
    return render_template('list.html', lst=lst, title='ChoiceList', form=form, chosen1=chosen1, chosen2=chosen2)

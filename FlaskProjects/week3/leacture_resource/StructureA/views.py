from flask import render_template, url_for
from app import app

@app.route("/")
def home():
    return render_template('home_learn.html', name='logesh')

@app.route('/mylist')
def mylist():
    list_test = ['Car', 'House', 'TV']
    return render_template('list_learn.html', list_test=list_test)

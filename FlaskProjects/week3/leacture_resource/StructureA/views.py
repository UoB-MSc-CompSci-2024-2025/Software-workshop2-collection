from flask import render_template, url_for
from app import app

@app.route("/")
def home():
    return render_template('home.html', name='Alan')

@app.route('/mylist')
def mylist():
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst)

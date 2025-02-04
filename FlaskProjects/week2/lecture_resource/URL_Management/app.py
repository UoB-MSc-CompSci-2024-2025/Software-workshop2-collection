from flask import Flask, render_template, url_for
from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    return render_template('home.html', name='Alan')

@app.route('/mylist')
def mylist():
    lst = ['Car', 'House', 'TV']
    return render_template('list.html', lst=lst)

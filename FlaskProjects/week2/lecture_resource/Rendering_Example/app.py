from flask import Flask, render_template
from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def hello():
    return "Hello, Alan!"

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           name=name,
                           title='Rendering Example')

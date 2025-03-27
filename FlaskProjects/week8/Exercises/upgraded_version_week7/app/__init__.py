import dateutil
from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

def debug(text):
  print(text)
  return ''

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.add_extension('jinja2.ext.debug')
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

app.jinja_env.filters['debug']=debug

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format)

from app import views, models

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, generate_password_hash=generate_password_hash)



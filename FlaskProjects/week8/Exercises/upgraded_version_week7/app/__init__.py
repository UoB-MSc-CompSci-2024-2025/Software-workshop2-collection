from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa
import sqlalchemy.orm as so


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

app.jinja_env.filters['debug'] = debug

from app import views, models
from app.debug_utils import reset_db, reset_product_db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db, generate_password_hash=generate_password_hash,
                reset_product_db=reset_product_db)

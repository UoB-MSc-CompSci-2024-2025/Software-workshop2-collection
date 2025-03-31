from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa
import sqlalchemy.orm as so


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import views, models
from app.debug_utils import reset_db

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)

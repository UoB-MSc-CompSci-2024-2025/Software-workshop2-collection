from flask import Flask
from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

app.config['SECRET_KEY'] = b'sedsfaey4335e35345sd'

from app import views

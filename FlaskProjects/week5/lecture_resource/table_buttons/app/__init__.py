from flask import Flask
from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = b'WR#&f&+%78er0we=%799eww+#7^90-;s'

from app import views
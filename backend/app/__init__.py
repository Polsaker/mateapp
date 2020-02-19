from flask import Flask, render_template, request
import sys

from .models import db_wrapper

from .views.token import token
from .common import JWT

try:
    import config
except ImportError:
    print("ERROR: El archivo de configuración no existe!")
    sys.exit(1)

app = Flask(__name__)
app.config.from_object('config')

# Inicialización de flaskdb
db_wrapper.init_app(app)
JWT.init_app(app)

# Inicialiación de todos los blueprint
app.register_blueprint(token, url_prefix='/token')
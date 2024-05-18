from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)

DEBUG = True
app.config["JWT_SECRET_KEY"] = 'ffiabfbfy241fsfeabkabdufvfafwfcsvasaeibe187wf322cwg5'

jwt_manager = JWTManager(app)
CORS(app)

DB_NAME = "Places.db"

from . import begin
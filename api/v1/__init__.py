from flask import Flask 
from datetime import timedelta
import dotenv
import os


app = Flask(__name__)

# .env management
ENVIRONMENT = os.getenv('ENVIRONMENT')

"""Database config"""
from flask_sqlalchemy import SQLAlchemy

if (ENVIRONMENT == "PRODUCTION"):
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PWD = os.getenv('MYSQL_PWD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(MYSQL_USER, MYSQL_PWD,
                                                                         MYSQL_HOST, MYSQL_DB)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)


""" cors for /api/v1"""
from flask_cors import CORS
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

"""Register Blueprint """
from v1.views import app_views
app.register_blueprint(app_views)

"""Uploading a file"""
UPLOAD_FOLDER_REVIEW = 'file/review'
UPLOAD_FOLDER_FEEDBACK = 'file/feedback'
ALLOWED_EXTENSIONS = {"txt"}

app.config['UPLOAD_FOLDER_REVIEW'] = UPLOAD_FOLDER_REVIEW
app.config['UPLOAD_FOLDER_FEEDBACK'] = UPLOAD_FOLDER_FEEDBACK


"""Secret key"""
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

"""Register flask uuid for generating random unique value"""
from flask_uuid import FlaskUUID
FlaskUUID(app)


"""JWT authentication"""

from flask_jwt_extended import JWTManager
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=48)
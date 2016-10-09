from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={"autoflush": False})

from app import views, models, tasks

# Logging einbauen
import logging
logging.basicConfig()

from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(app.config['LOG_FILE'], 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
file_handler.setLevel(logging.INFO)

app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)


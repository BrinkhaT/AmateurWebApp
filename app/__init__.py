from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={"autoflush": False})

from app import views, models, tasks

# Logging einbauen
import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig()
file_handler = RotatingFileHandler('logs/webapp.log', 'a', 1 * 1024 * 1024, 10)
#file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('AmateurWebApp startup')

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOG_FILE = os.path.join(basedir, 'logs/webapp.log')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DiesIstMeineKleineAppUndDasIstStrengGeheim'

# Konfiguration fuer alle Jobs
JOB_VARIATION = 0.3 # Variation der Zeitpunkt +- 30%
JOB_FIVE_INTERVAL = 300
JOB_HOUR_INTERVAL_START = 120
JOB_HOUR_INTERVAL = 1800

# Einstellungen fuer den Job retweetAndDeleteTweets
JOB_RETWEET_AMOUNT = 2

# Einstellungen fuer den Job retweetAndDeleteTweets
JOB_CHECKTWITTER_INITIALLOAD = 3

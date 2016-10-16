import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOG_FILE = os.path.join(basedir, 'logs/webapp.log')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DiesIstMeineKleineAppUndDasIstStrengGeheim'

#Konfiguration fuer die regelmaessigen Jobs
JOB_VARIATION = 0.3 # Variation der Zeitpunkt +- 30%
JOB_INTERVAL_SEC_RETWEET = 300 #Job retweetAndDeleteTweets aller 5 Min
JOB_INTERVAL_SEC_CHECKFOLLOWER = 3600 #Job checkFollowerForUpdates jede Stunde
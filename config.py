import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'DiesIstMeineKleineAppUndDasIstStrengGeheim'

JOBS = [
        {
            'id': 'job_checkFollowerForUpdates',
            'func': 'app.tasks:checkFollowerForUpdates',
            'args': None,
            'trigger': 'interval',
            'minutes': 5
        },
        {
            'id': 'job_retweetAndDeleteTweets',
            'func': 'app.tasks:retweetAndDeleteTweets',
            'args': None,
            'trigger': 'interval',
            'minutes': 3
        }
    ]
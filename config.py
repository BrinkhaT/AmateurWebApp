import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JOBS = [
        {
            'id': 'job1',
            'func': 'app.tasks:doSomeMagic',
            'args': None,
            'trigger': 'interval',
            'seconds': 60
        }
    ]
#!flask/bin/python
from app import app, tasks
from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

tasks.checkFollowerForUpdates()
tasks.retweetAndDeleteTweets()

app.logger.info('Scheduler started, start WebApp')
app.run(debug=True, host="0.0.0.0", use_reloader=False)
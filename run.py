#!/home/pi/AmateurWebApp/flask/bin/python
from app import app, tasks, taskHelper

app.scheduler.init_app(app)
app.scheduler.start()

# Jobs zum Scheduler hinzufuegen
nextStart = taskHelper.calc_next_start_time(app.config['JOB_INTERVAL_SEC_RETWEET'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.retweetAndDeleteTweets, trigger='date', run_date=nextStart, id="retweetAndDeleteTweets")
app.logger.info("retweetAndDeleteTweets: naechster Start = " + repr(nextStart))

nextStart = taskHelper.calc_next_start_time(app.config['JOB_INTERVAL_SEC_CHECKFOLLOWER'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.checkFollowerForUpdates, trigger='date', run_date=nextStart, id="checkFollowerForUpdates")
app.logger.info("checkFollowerForUpdates: naechster Start = " + repr(nextStart))

app.logger.info('Scheduler started, start WebApp')
app.run(debug=True, host="0.0.0.0", use_reloader=False)

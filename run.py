#!/home/pi/AmateurWebApp/flask/bin/python
from app import app, tasks, taskHelper, rssHelper

app.scheduler.init_app(app)
app.scheduler.start()

# Jobs zum Scheduler hinzufuegen
nextStart = taskHelper.calc_next_start_time(app.config['JOB_RETWEET_INTERVAL'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.retweetAndDeleteTweets, trigger='date', run_date=nextStart, id="retweetAndDeleteTweets")
app.logger.info("retweetAndDeleteTweets: naechster Start = " + repr(nextStart))

nextStart = taskHelper.calc_next_start_time(app.config['JOB_CHECKTWITTER_INTERVAL_START'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.checkFollowerForUpdates, trigger='date', run_date=nextStart, id="checkFollowerForUpdates")
app.logger.info("checkFollowerForUpdates: naechster Start = " + repr(nextStart))

interval = app.config['JOB_MDHNEWRSS_INTERVAL']
app.scheduler.add_job(func=rssHelper.loadAndSaveMdhVids, trigger='interval', minutes=, id="loadAndSaveMdhVids")
app.logger.info("loadAndSaveMdhVids: gestartet, Intervall: %i Minuten" % (interval))

app.logger.info('Scheduler started, start WebApp')
app.run(debug=False, host="0.0.0.0", use_reloader=False)

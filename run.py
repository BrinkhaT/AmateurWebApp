#!/home/pi/AmateurWebApp/flask/bin/python
from app import app, tasks, taskHelper, rssHelper

app.scheduler.init_app(app)
app.scheduler.start()

# Jobs zum Scheduler hinzufuegen
nextStart = taskHelper.calc_next_start_time(app.config['JOB_FIVE_INTERVAL'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.jobsEveryFiveMinutes, trigger='date', run_date=nextStart, id="jobsEveryFiveMinutes")
app.logger.info("jobsEveryFiveMinutes: naechster Start = " + repr(nextStart))

nextStart = taskHelper.calc_next_start_time(app.config['JOB_HOUR_INTERVAL_START'], app.config['JOB_VARIATION'])
app.scheduler.add_job(func=tasks.jobsEveryHour, trigger='date', run_date=nextStart, id="jobsEveryHour")
app.logger.info("jobsEveryHour: naechster Start = " + repr(nextStart))

app.logger.info('Scheduler started, start WebApp')
app.run(debug=False, host="0.0.0.0", use_reloader=False)

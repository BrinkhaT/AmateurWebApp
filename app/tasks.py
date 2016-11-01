from app import app, db, models, twitter, AmateurHelper, taskHelper, rssHelper
from datetime import datetime
import tweepy
import json

def jobsEveryFiveMinutes():
	app.logger.info("jobsEveryFiveMinutes: Start")
	
	nextStart = taskHelper.calc_next_start_time(app.config['JOB_FIVE_INTERVAL'], app.config['JOB_VARIATION'])
	app.scheduler.add_job(func=jobsEveryFiveMinutes, trigger='date', run_date=nextStart, id="jobsEveryFiveMinutes")
	app.logger.info("jobsEveryFiveMinutes: naechster Start = " + repr(nextStart))
	
	rssHelper.loadAndSaveMdhVids()
	retweetAndDeleteTweets()
	
	app.logger.info("jobsEveryFiveMinutes: Ende")
	
def jobsEveryHour():
	app.logger.info("jobsEveryHour: Start")
	
	nextStart = taskHelper.calc_next_start_time(app.config['JOB_HOUR_INTERVAL'], app.config['JOB_VARIATION'])
	app.scheduler.add_job(func=jobsEveryHour, trigger='date', run_date=nextStart, id="jobsEveryHour")
	app.logger.info("jobsEveryHour: naechster Start = " + repr(nextStart))	
	
	rssHelper.loadAndTweetPPPVids()
	checkFollowerForUpdates()
	
	app.logger.info("jobsEveryHour: Ende")

def runRssChecks():
	app.logger.info("runRssChecks: Start")
	
	rssHelper.loadAndSaveMdhVids()
	rssHelper.loadAndTweetPPPVids()
	
	app.logger.info("runRssChecks: Ende")

def checkFollowerForUpdates():
	app.logger.info("checkFollowerForUpdates: Start")
	
	initialLoad = app.config['JOB_CHECKTWITTER_INITIALLOAD']
	
	for acc in db.session.query(models.TwitterAccount).all():
		app.logger.info("checkFollowerForUpdates: Start Twitter Config %r" % (acc))
		wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
			accessSecret=acc.twAccessSecret)

		for f in db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twConfig == acc.id).order_by(models.TwitterFollower.lastChecked).all():
			app.logger.info("checkFollowerForUpdates: Start Users %r" % (f))

			sSet = []
			if f.lastChecked == None or f.twLastId == None:
				sSet = wrapper.getStatusForUserLimited(f.twName, initialLoad)
			else:
				sSet = wrapper.getStatusForUserSinceLastUpdate(f.twName, f.twLastId)

			counter = 0
			try:
				for s in sSet:
					if s.retweeted == False and db.session.query(models.TweetsToRetweet).get(s.id) == None:
						t = models.TweetsToRetweet(id=s.id, twConfig=acc.id, tweetOwner=s.user.screen_name, 
								tweetText=s.text)
						counter += 1
	
						if f.twLastId == None:
							f.twLastId = s.id
						else:
							f.twLastId = max(f.twLastId, s.id)
	
						db.session.add(t)
	
				f.lastChecked = datetime.utcnow()
				db.session.add(f)
				db.session.commit()
			except tweepy.TweepError as e:
				error = json.loads(e.response.content)
				if error['errors'][0]['code'] == 88:
					app.logger.error('checkFollowerForUpdates: Zu viele API Zugriffe. Abbruch!')
					break
				else:
					app.logger.error('checkFollowerForUpdates: Es ist ein Twitter-Fehler aufgetreten: : %s (%i)' % (error['errors'][0]['message'], error['errors'][0]['code']))
					pass
			
			app.logger.info("checkFollowerForUpdates: Ende Users %r: Geladene Tweets %r" % (f, counter))
		app.logger.info("checkFollowerForUpdates: Ende Twitter Config %r" % (acc))
	
	app.logger.info("checkFollowerForUpdates: Ende")

def retweetAndDeleteTweets():
	app.logger.info("retweetAndDeleteTweets: Start")
	
	for acc in models.TwitterAccount.query.all():
		app.logger.info("retweetAndDeleteTweets: Start Twitter Config %r" % (acc))

		wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
			accessSecret=acc.twAccessSecret)

		tSet = db.session.query(models.TweetsToRetweet).filter(models.TweetsToRetweet.twConfig == acc.id).order_by(models.TweetsToRetweet.id).limit(2)

		counter = 0
		for t in tSet:
			wrapper.retweet(t.id)
			#wrapper.updateStatus("Test mehr hier: http://www.google.de https://twitter.com/ABikerBar/status/" + str(t.id))
			db.session.delete(t)
			counter = counter + 1
			
		db.session.commit()
		app.logger.info("retweetAndDeleteTweets: Ende Twitter Config %r: Retweets %r" % (acc, counter))

	app.logger.info("retweetAndDeleteTweets: Ende")
	
def lowerCaseTwitterFollower():
	for t in db.session.query(models.TwitterFollower).all():
		t.twName = t.twName.lower()
		db.session.add(t)
	db.session.commit()	
	
def addAllTwitterFollower():
	for acc in models.TwitterAccount.query.all():
		wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
			accessSecret=acc.twAccessSecret)
		
		try:
			for f in wrapper.getFollowers():
				twName = f.screen_name.lower()
				
				if db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twName == twName and models.TwitterFollower.twConfig == acc.id).first() == None:
					if acc.id == 2:
						AmateurHelper.createAmateurByTwitterName(twName)
					else:
						t = models.TwitterFollower(twName=twName, twConfig=acc.id)
						db.session.add(t)
				
			db.session.commit()
		except tweepy.TweepError as e:
			app.logger.error('Der bei Abruf der Twitter-Freunde: %s (Code: %s)' % (e[0][0]['message'], e[0][0]['code']))
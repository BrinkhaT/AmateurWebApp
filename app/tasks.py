from app import app, db, models, twitter
from datetime import datetime

def checkFollowerForUpdates():
	app.logger.info("checkFollowerForUpdates: Start")
	for acc in db.session.query(models.TwitterAccount).all():
		app.logger.info("checkFollowerForUpdates: Start Twitter Config %r" % (acc))
		wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
			accessSecret=acc.twAccessSecret)

		for f in db.session.query(models.TwitterFollower).filter(models.TwitterFollower.twConfig == acc.id).order_by(models.TwitterFollower.lastChecked).limit(10).all():
			app.logger.info("checkFollowerForUpdates: Start Users %r" % (f))

			sSet = []
			if f.lastChecked == None or f.twLastId == None:
				sSet = wrapper.getStatusForUserLimited(f.twName, 3)
			else:
				sSet = wrapper.getStatusForUserSinceLastUpdate(f.twName, f.twLastId)

			counter = 0
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

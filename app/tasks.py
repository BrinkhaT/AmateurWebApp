from app import app, db, models, twitter, AmateurHelper
from datetime import datetime
import tweepy

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
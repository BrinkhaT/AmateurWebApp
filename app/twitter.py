import tweepy
from app import app

class TwitterHelper:
	api = None

	def __init__(self, consKey, consSecret, accessToken, accessSecret):
		self.consKey = consKey
		self.consSecret = consSecret
		self.accessToken = accessToken
		self.accessSecret = accessSecret

	def initiateApi(self):
		auth = tweepy.OAuthHandler(self.consKey, self.consSecret)
		auth.set_access_token(self.accessToken, self.accessSecret)
		
		try:
			self.api = tweepy.API(auth)
		except tweepy.TweepError as e:
			app.logger.error('Fehler beim Verbinden zu Twitter: %s (Code: %s)' % (e[0][0]['message'], e[0][0]['code']))
			return False
			
		return True

	def retweet(self, statusId):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		try:
			self.api.retweet(statusId)
		except tweepy.TweepError as e:
			app.logger.error('Fehler beim Retweeten: %s (Code: %s)' % (e[0][0]['message'], e[0][0]['code']))
			return False
		
		return True

	def updateStatus(self, text):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		try:
			self.api.update_status(status=text)
		except tweepy.TweepError as e:
			app.logger.error('Fehler beim Statusupdate: %s (Code: %s)' % (e[0][0]['message'], e[0][0]['code']))
			return False
		
		return True

	def getRateLimitStatus(self):
		try:
			return self.api.rate_limit_status()
		except tweepy.TweepError as e:
			app.logger.error('Fehler Auslesen der Limits: %s (Code: %s)' % (e[0][0]['message'], e[0][0]['code']))
			return None

	def checkRateLimitForUserTimeline(self):
		status = self.getRateLimitStatus()
		if status == None:
			return False
		elif status['resources']['statuses']['/statuses/user_timeline']['remaining'] > 0:
			return True
		return False
		
	def validateUser(self, screen_name):
		if self.api == None:
			if self.initiateApi() == False:
				return False
		
		try:
			self.api.get_user(screen_name=screen_name)
		except  tweepy.TweepError as e:
			app.logger.error('Der bei Abruf des Twitter-Nutzers %r: %s (Code: %s)' % (screen_name, e[0][0]['message'], e[0][0]['code']))
			return False
		
		try:
			self.api.user_timeline(screen_name=screen_name, count=1)
		except tweepy.TweepError as e: 
			app.logger.error('Fehler beim Abruf der Tweets von Nutzer %s: %s (Code: %s)' % (screen_name, e[0][0]['message'], e[0][0]['code']))
			return False
		
		return True

	def getStatusForUserLimited(self, screen_name, limit):
		if self.api == None:
			if self.initiateApi() == False:
				return False
		
		if self.checkRateLimitForUserTimeline() and self.validateUser(screen_name):
			return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name).items(limit)
		return []

	def getStatusForUserSinceLastUpdate(self, screen_name, since_id):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		if self.checkRateLimitForUserTimeline() and self.validateUser(screen_name):
			return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, since_id=since_id).items()
		return []
	
	def getFollowers(self):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		return tweepy.Cursor(self.api.friends).items() 
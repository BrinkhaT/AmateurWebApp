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
		self.api = tweepy.API(auth)

	def retweet(self, statusId):
		if self.api == None:
			self.initiateApi()
		self.api.retweet(statusId)
		return True

	def updateStatus(self, text):
		if self.api == None:
			self.initiateApi()
		self.api.update_status(status=text)
		return True

	def getRateLimitStatus(self):
		return self.api.rate_limit_status()

	def checkRateLimitForUserTimeline(self):
		status = self.getRateLimitStatus()
		if status['resources']['statuses']['/statuses/user_timeline']['remaining'] > 0:
			return True
		return False
		
	def validateUser(self, screen_name):
		if self.api == None:
			self.initiateApi()
		
		try:
			get_user(self.api.screen_name)
			return True
		except:
			app.logger.error('Es ist ein Fehler bei der Pruefung des Twitter Nutzers %r aufgetreten' % (screen_name))
		return False

	def getStatusForUserLimited(self, screen_name, limit):
		if self.api == None:
			self.initiateApi()
		
		if self.checkRateLimitForUserTimeline() and self.validateUser(screen_name):
			return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name).items(limit)
		return []

	def getStatusForUserSinceLastUpdate(self, screen_name, since_id):
		if self.api == None:
			self.initiateApi()
			
		if self.checkRateLimitForUserTimeline() and self.validateUser(screen_name):
			return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, since_id=since_id).items()
		return []
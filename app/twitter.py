import tweepy

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

	def getStatusForUserLimited(self, screen_name, limit):
		if self.api == None:
			self.initiateApi()
		return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name).items(limit)

	def getStatusForUserSinceLastUpdate(self, screen_name, since_id):
		if self.api == None:
			self.initiateApi()
		return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, since_id=since_id).items()
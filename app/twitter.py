import tweepy
import requests
import os
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

	def updateStatusWithPic(self, text, urlToPic):
		if not urlToPic:
			self.updateStatus(text=text)
		
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		try:
			basedir = os.path.abspath(os.path.dirname(__file__))
			filename = os.path.join(basedir, 'temp.jpg')
			request = requests.get(urlToPic, stream=True)
			if request.status_code == 200:
				with open(filename, 'wb') as image:
					for chunk in request:
						image.write(chunk)

		        self.api.update_with_media(filename, status=text)
		        os.remove(filename)
		except tweepy.TweepError as e:
			os.remove(filename)
			app.logger.error('Fehler beim Statusupdate: %r ' % (e))
			return False
		
		return True

	def getStatusForUserLimited(self, screen_name, limit):
		if self.api == None:
			if self.initiateApi() == False:
				return False
		
		return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name).items(limit)

	def getStatusForUserSinceLastUpdate(self, screen_name, since_id):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		return tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, since_id=since_id).items()
	
	def getFollowers(self):
		if self.api == None:
			if self.initiateApi() == False:
				return False
			
		return tweepy.Cursor(self.api.friends).items() 
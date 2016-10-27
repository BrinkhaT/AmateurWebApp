from app import app, db, models, twitter
from datetime import datetime, timedelta, tzinfo
import urllib2
import xmltodict
import pytz

def loadAndSaveMdhVids():
    acc = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 2).first()
    if acc:
        wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
            accessSecret=acc.twAccessSecret)
        
        rssSet = db.session.query(models.RssFeed).filter(models.RssFeed.function == 'mdhNewVids').all()
        for rss in rssSet:
            now = datetime.now()
            lastChecked = rss.lastChecked
            
            file = urllib2.urlopen(rss.feedUrl)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
            
            for i in data['rss']['channel']['item']:
                i = mdhItem(i)
                
                if not lastChecked or i.vidPubDate > lastChecked:
                    amateur = db.session.query(models.Amateur).filter(models.Amateur.mdhId == i.mdhId).first()
                    if amateur:
                        text = 'Geiles neues Video von %s: %s' % (i.mdhUser, i.vidLink)
                        wrapper.updateStatusWithPic(text=text, urlToPic=i.vidImg)
                        app.logger.info('loadAndSaveMdhVids: neues Video eines Amateurs: %s' % (text))
                
            rss.lastChecked = now
            db.session.add(rss)
            db.session.commit()
            
class mdhItem:
    def __init__(self, i):
        self.vidTitel = i['title']
        self.vidId = i['uv_id']
        self.mdhUser = i['u_nick']
        self.mdhId = i['u_id']
        self.vidLink = i['link']
        
        imgSmall = i['video_img']
        self.vidImg = imgSmall.replace('.jpg', '_sc_orig.jpg')
        
        pubDateStr = str(i['pubDate'])
        self.vidPubDate = datetime.strptime(pubDateStr[:-6], '%a, %d %b %Y %H:%M:%S')
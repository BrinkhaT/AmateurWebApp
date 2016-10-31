from app import app, db, models, twitter, bitly
from datetime import datetime, timedelta, tzinfo
import urllib2
import xmltodict
import pytz
import re

def loadAndSaveMdhVids():
    app.logger.info("loadAndSaveMdhVids: Start")
    acc = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 2).first()
    if acc:
        wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
            accessSecret=acc.twAccessSecret)
        
        rssSet = db.session.query(models.RssFeed).filter(models.RssFeed.function == 'mdhNewVids').all()
        for rss in rssSet:
            now = datetime.now()
            lastChecked = rss.lastChecked
            
            newVids = []
            for i in getMdhItems(rss.feedUrl):
                if not lastChecked or i.vidPubDate > lastChecked:
                    newVids.append('%s (%s)' % (i.mdhUser, i.mdhId))
                    amateur = db.session.query(models.Amateur).filter(models.Amateur.mdhId == i.mdhId).first()
                    if amateur:
                        shortLink = bitly.shortenUrl(i.vidLink)
                        if amateur.tw:
                            text = 'Geiles neues Video von @%s: %s' % (amateur.tw, shortLink)
                        else:
                            text = 'Geiles neues Video von %s: %s' % (i.mdhUser, shortLink)
                        
                        wrapper.updateStatusWithPic(text=text, urlToPic=i.vidImg)
                        app.logger.info('loadAndSaveMdhVids: neues Video eines Amateurs: %s' % (text))
                
            app.logger.info('loadAndSaveMdhVids: im Feed enthaltene User: %s' % (', '.join(newVids)))
            rss.lastChecked = now
            db.session.add(rss)
            db.session.commit()
            
    app.logger.info("loadAndSaveMdhVids: Ende")
    
def getMdhItems(url):
    items = []
    data = getDataFromRssFeed(url)
    
    if data:
        for i in data['rss']['channel']['item']:
            i = mdhItem(i)
            items.append(i)
    
    return items
            
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
        
def loadAndTweetPPPVids():
    app.logger.info("loadAndTweetPPPVids: Start")
    acc = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 2).first()
    if acc:
        wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
            accessSecret=acc.twAccessSecret)
        
        amateurSet = db.session.query(models.Amateur).filter(models.Amateur.pmId.isnot(None)).all()
        for amateur in amateurSet:
            if amateur.pmId and amateur.pmRef:
                url = 'http://ppp.pornme.com/%s/m/rss/videos/?ref=%s' % (amateur.pmId, amateur.pmRef)
                app.logger.info('loadAndTweetPPPVids: pruefe Feed von %s (%s)' % (amateur.name, url))
                data = getPPPItems(url)
                now = datetime.now()
                lastChecked = amateur.pmLastChecked
                
                if not lastChecked:
                    counter = 0
                    for i in data:
                        if counter < 3:
                            shortLink = bitly.shortenUrl(i.vidLink)
                            if amateur.tw:
                                text = 'Geiles neues Video von @%s: %s' % (amateur.tw, shortLink)
                            else:
                                text = 'Geiles neues Video von %s: %s' % (i.mdhUser, shortLink)
                            
                            wrapper.updateStatusWithPic(text=text, urlToPic=i.vidImg)
                            app.logger.info('loadAndTweetPPPVids: neues Video eines Amateurs: %s' % (text))
                            counter = counter + 1
                        else:
                            break
                else:
                    for i in data:
                        if i.vidPubDate > lastChecked:
                            shortLink = bitly.shortenUrl(i.vidLink)
                            if amateur.tw:
                                text = 'Geiles neues Video von @%s: %s' % (amateur.tw, shortLink)
                            else:
                                text = 'Geiles neues Video von %s: %s' % (i.mdhUser, shortLink)
                            
                            wrapper.updateStatusWithPic(text=text, urlToPic=i.vidImg)
                            app.logger.info('loadAndTweetPPPVids: neues Video eines Amateurs: %s' % (text))
                amateur.pmLastChecked = now
                db.session.add(amateur)
                db.session.commit()            
        
    app.logger.info("loadAndTweetPPPVids: Ende")
    
def getPPPItems(url):
    items = []
    data = getDataFromRssFeed(url)
    
    if data:
        for i in data['rss']['channel']['item']:
            i = pppItem(i)
            items.append(i)
    
    return items

class pppItem:
    def __init__(self, i):
        self.vidTitel = i['title']
        self.pppUser = i['author']
        self.vidLink = i['link']
        
        self.vidImg = None
        
        desc = i['description']
        p = re.compile('^.*img src=\"(.*)\" width.*$')
        m = p.match(desc)
        
        if m:
            self.vidImg = m.group(1)
        
        pubDateStr = str(i['pubDate'])
        self.vidPubDate = datetime.strptime(pubDateStr[:-6], '%a, %d %b %Y %H:%M:%S')

def getDataFromRssFeed(url):
    try:
        file = urllib2.urlopen(url)
        data = file.read()
        file.close()
        data = xmltodict.parse(data)
        return data
    except:
        app.logger.error('Fehler beim Parsen des RSS Feeds')
        return None
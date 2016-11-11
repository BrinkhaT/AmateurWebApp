from app import app, db, models, twitter, bitly
from datetime import datetime, timedelta, tzinfo
from operator import attrgetter
import urllib2
import xmltodict
import pytz
import re

def publishNewVid(wrapper, vidLink, vidImg, aName, proc):
    shortLink = bitly.shortenUrl(vidLink)
    text = 'Geiles neues #Video von %s: %s #porn #xxx #amateur' % (aName, shortLink)
    
    if wrapper.updateStatusWithPic(text=text, urlToPic=vidImg):
        app.logger.info('%s: neues Video eines Amateurs: %s' % (proc, text))
    else:
        app.logger.error('%s: neues Video eines Amateurs (%s) konnte nicht veroeffentlicht werden' % (proc, text))

def loadAndSaveMdhVids():
    app.logger.info("loadAndSaveMdhVids: Start")
    acc = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 2).first()
    accAllFeeds = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 3).first()
    if acc:
        wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
            accessSecret=acc.twAccessSecret)
        
        wrapperAll = twitter.TwitterHelper(consKey=accAllFeeds.twConsKey, consSecret=accAllFeeds.twConsSecret, 
                                            accessToken=accAllFeeds.twAccessToken, accessSecret=accAllFeeds.twAccessSecret)
        
        rssSet = db.session.query(models.RssFeed).filter(models.RssFeed.function == 'mdhNewVids').all()
        for rss in rssSet:
            lastChecked = rss.lastChecked
            newestVid = lastChecked
            
            newVids = []
            for i in getMdhItems(rss.feedUrl):
                if not lastChecked or i.vidPubDate > lastChecked:
                    newestVid = i.vidPubDate
                    newVids.append('%s (%s)' % (i.mdhUser, i.mdhId))
                    amateur = db.session.query(models.Amateur).filter(models.Amateur.mdhId == i.mdhId).first()
                    if amateur:
                        publishNewVid(wrapper, i.vidLink, i.vidImg, i.mdhUser, 'loadAndSaveMdhVids')
                    if wrapperAll:
                        publishNewVid(wrapperAll, i.vidLink, i.vidImg, i.mdhUser, 'loadAndSaveMdhVids_ALL')
                        
            app.logger.info('loadAndSaveMdhVids: im Feed enthaltene User: %s' % (', '.join(newVids)))
            rss.lastChecked = newestVid
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
            
    items = sorted(items, key=attrgetter('vidPubDate'))
    
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
        
    def __repr__(self):
        return '<MdhItem %s: %s (%s)>' % (self.mdhUser, self.vidTitel, self.vidPubDate)
        
def loadAndTweetPPPVids():
    app.logger.info("loadAndTweetPPPVids: Start")
    acc = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 2).first()
    accAllFeeds = db.session.query(models.TwitterAccount).filter(models.TwitterAccount.id == 3).first()
    if acc:
        wrapper = twitter.TwitterHelper(consKey=acc.twConsKey, consSecret=acc.twConsSecret, accessToken=acc.twAccessToken, 
            accessSecret=acc.twAccessSecret)
        wrapperAll = twitter.TwitterHelper(consKey=accAllFeeds.twConsKey, consSecret=accAllFeeds.twConsSecret, 
                                            accessToken=accAllFeeds.twAccessToken, accessSecret=accAllFeeds.twAccessSecret)
        
        amateurSet = db.session.query(models.Amateur).filter(models.Amateur.pmId.isnot(None)).all()
        for amateur in amateurSet:
            if amateur.pmId and amateur.pmRef:
                url = 'http://ppp.pornme.com/%s/m/rss/videos/?ref=%s' % (amateur.pmId, amateur.pmRef)
                app.logger.info('loadAndTweetPPPVids: pruefe Feed von %s (%s)' % (amateur.name, url))
                data = getPPPItems(url)

                lastChecked = amateur.pmLastChecked
                newestVid = lastChecked
                
                counter = 0
                for i in data:
                    if not lastChecked or i.vidPubDate > lastChecked:
                        if counter >= 1:
                            break
                        else:
                            newestVid = i.vidPubDate
                            publishNewVid(wrapper, i.vidLink, i.vidImg, i.pppUser, 'loadAndTweetPPPVids')
                            counter = counter + 1
                            
                            if wrapperAll:
                                publishNewVid(wrapper, i.vidLink, i.vidImg, i.pppUser, 'loadAndTweetPPPVids_ALL')

                amateur.pmLastChecked = newestVid
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
            
    items = sorted(items, key=attrgetter('vidPubDate'))
    
    return items

class pppItem:
    def __init__(self, i):
        self.vidTitel = i['title']
        self.pppUser = i['author']
        self.vidLink = i['link']
        
        self.vidImg = None
        
        desc = i['description']
        desc = ' '.join(desc.split())
        p = re.compile('^.*img src=\"(.*)\" width.*$')
        m = p.match(desc)
        
        if m:
            self.vidImg = m.group(1)
            
            p = re.compile('^(.*)(_320_180_)(.*)$')
            m = p.match(self.vidImg)
            
            if m:
                self.vidImg = m.group(1) + '_1280_720_' + m.group(3)
            else:
                p = re.compile('^(.*)(\/16_9\/large\/)(.*)$')
                m = p.match(self.vidImg)
                
                if m:
                    self.vidImg = m.group(1) + '/original/' + m.group(3)
        
        pubDateStr = str(i['pubDate'])
        self.vidPubDate = datetime.strptime(pubDateStr[:-6], '%a, %d %b %Y %H:%M:%S')
        
        def __repr__(self):
            return '<pppItem %s: %s (%s)>' % (self.pppUser, self.vidTitel, self.vidPubDate)

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
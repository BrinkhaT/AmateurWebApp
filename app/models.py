from app import db

class Amateur(db.Model):
    __tablename__ = "amateure"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    tw = db.Column(db.String(15))
    mdhId = db.Column(db.String(30))
    vxId = db.Column(db.String(30))
    pmId = db.Column(db.String(30))
    pmRef = db.Column(db.String(30))
    pmLastChecked = db.Column(db.DateTime)
    subDomain = db.Column(db.String(30))

    def __repr__(self):
        return '<Amateur %r>' % (self.name)

class TweetsToRetweet(db.Model):
    __tablename__ = "twitter_open_retweets"
    id = db.Column(db.BigInteger, primary_key=True)
    twConfig = db.Column(db.Integer, db.ForeignKey('twitter_accounts.id'), nullable=False)
    tweetOwner = db.Column(db.String(15), nullable=False)
    tweetText = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<TweetsToRetweet %r: %r>' % (self.tweetOwner, self.tweetText)

class TwitterFollower(db.Model):
    __tablename__ = "twitter_follower"
    id = db.Column(db.Integer, primary_key=True)
    twName = db.Column(db.String(15), index=True, unique=True, nullable=False)
    twConfig = db.Column(db.Integer, db.ForeignKey('twitter_accounts.id'), nullable=False)
    lastChecked = db.Column(db.DateTime)
    twLastId = db.Column(db.BigInteger)

    def __repr__(self):
        return '<TwitterFollower %r>' % (self.twName)

class TwitterAccount(db.Model):
    __tablename__ = 'twitter_accounts'
    id = db.Column(db.Integer, primary_key=True)
    twId = db.Column(db.String(30), unique=True)
    twName = db.Column(db.String(15), unique=True)
    twAccessToken = db.Column(db.String(50))
    twAccessSecret = db.Column(db.String(50))
    twConsKey = db.Column(db.String(50))
    twConsSecret = db.Column(db.String(50))

    def __repr__(self):
        return '<TwitterAccount %r (%r)>' % (self.twName, self.id)

class RssFeed(db.Model):
    __tablename__ = 'rss_feeds'
    id = db.Column(db.Integer, primary_key=True)
    feedName = db.Column(db.String(150))
    feedUrl = db.Column(db.String(150), unique=True, nullable=False)
    lastChecked = db.Column(db.DateTime)
    lastId = db.Column(db.BigInteger)
    function = db.Column(db.String(50))
    
    def __repr__(self):
        return '<RssFeed %r (%s)>' % (self.feedName, self.lastChecked)
    
class SysProp(db.Model):
    __tablename__ = 'sys_props'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    value = db.Column(db.String(200), unique=True, nullable=False)
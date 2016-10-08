from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tweets_to_retweet = Table('tweets_to_retweet', pre_meta,
    Column('id', BIGINT, primary_key=True, nullable=False),
    Column('twConfig', INTEGER),
    Column('tweetOwner', VARCHAR(length=15), nullable=False),
    Column('tweetText', VARCHAR(length=150), nullable=False),
    Column('retweeted', BOOLEAN, nullable=False),
)

twitteraccount = Table('twitteraccount', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('twId', VARCHAR(length=30)),
    Column('twName', VARCHAR(length=15)),
    Column('twAccessToken', VARCHAR(length=50)),
    Column('twAccessSecret', VARCHAR(length=50)),
    Column('twConsKey', VARCHAR(length=50)),
    Column('twConsSecret', VARCHAR(length=50)),
)

twitter_accounts = Table('twitter_accounts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('twId', String(length=30)),
    Column('twName', String(length=15)),
    Column('twAccessToken', String(length=50)),
    Column('twAccessSecret', String(length=50)),
    Column('twConsKey', String(length=50)),
    Column('twConsSecret', String(length=50)),
)

twitter_follower = Table('twitter_follower', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('twName', String(length=15)),
    Column('lastChecked', DateTime),
    Column('twLastId', BigInteger),
)

twitter_open_retweets = Table('twitter_open_retweets', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('twConfig', Integer),
    Column('tweetOwner', String(length=15), nullable=False),
    Column('tweetText', String(length=150), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tweets_to_retweet'].drop()
    pre_meta.tables['twitteraccount'].drop()
    post_meta.tables['twitter_accounts'].create()
    post_meta.tables['twitter_follower'].create()
    post_meta.tables['twitter_open_retweets'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tweets_to_retweet'].create()
    pre_meta.tables['twitteraccount'].create()
    post_meta.tables['twitter_accounts'].drop()
    post_meta.tables['twitter_follower'].drop()
    post_meta.tables['twitter_open_retweets'].drop()

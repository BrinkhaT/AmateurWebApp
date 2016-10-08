from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateur_tweets = Table('amateur_tweets', pre_meta,
    Column('id', BIGINT, primary_key=True, nullable=False),
    Column('retweeted', BOOLEAN, nullable=False),
)

tweets_to_retweet = Table('tweets_to_retweet', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('twConfig', Integer),
    Column('tweetOwner', String(length=15), nullable=False),
    Column('tweetText', String(length=150), nullable=False),
    Column('retweeted', Boolean, nullable=False, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur_tweets'].drop()
    post_meta.tables['tweets_to_retweet'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur_tweets'].create()
    post_meta.tables['tweets_to_retweet'].drop()

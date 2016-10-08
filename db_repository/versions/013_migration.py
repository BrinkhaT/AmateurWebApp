from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
twitter_account = Table('twitter_account', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('twId', VARCHAR(length=30)),
    Column('twName', VARCHAR(length=15)),
    Column('twAccessToken', VARCHAR(length=50)),
    Column('twAccessSecret', VARCHAR(length=50)),
    Column('twConsKey', VARCHAR(length=50)),
    Column('twConsSecret', VARCHAR(length=50)),
)

twitteraccount = Table('twitteraccount', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('twId', String(length=30)),
    Column('twName', String(length=15)),
    Column('twAccessToken', String(length=50)),
    Column('twAccessSecret', String(length=50)),
    Column('twConsKey', String(length=50)),
    Column('twConsSecret', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['twitter_account'].drop()
    post_meta.tables['twitteraccount'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['twitter_account'].create()
    post_meta.tables['twitteraccount'].drop()

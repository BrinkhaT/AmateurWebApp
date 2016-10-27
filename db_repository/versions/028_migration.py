from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
rss_feeds = Table('rss_feeds', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('feedName', String(length=150)),
    Column('feedUrl', String(length=150), nullable=False),
    Column('lastChecked', DateTime),
    Column('lastId', BigInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['rss_feeds'].columns['feedName'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['rss_feeds'].columns['feedName'].drop()

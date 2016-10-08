from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
twitter_account = Table('twitter_account', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('twId', String(length=30)),
    Column('twName', String(length=15)),
    Column('twAccessToken', String(length=50)),
    Column('twAccessSecret', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['twitter_account'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['twitter_account'].drop()

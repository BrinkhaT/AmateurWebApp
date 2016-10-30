from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateure = Table('amateure', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('tw', String(length=15)),
    Column('mdhId', String(length=30)),
    Column('vxId', String(length=30)),
    Column('pmId', String(length=30)),
    Column('pmRef', String(length=30)),
    Column('pmLastChecked', DateTime),
    Column('subDomain', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amateure'].columns['pmLastChecked'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amateure'].columns['pmLastChecked'].drop()

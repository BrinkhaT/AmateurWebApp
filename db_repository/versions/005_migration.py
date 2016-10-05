from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateur = Table('amateur', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('twitter', VARCHAR(length=30)),
    Column('mdhLink', VARCHAR(length=120)),
    Column('pmLink', VARCHAR(length=120)),
    Column('subDomain', VARCHAR(length=30)),
    Column('vxLink', VARCHAR(length=120)),
    Column('mdhId', VARCHAR(length=30)),
)

amateur = Table('amateur', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('twitter', String(length=30)),
    Column('mdhId', String(length=30)),
    Column('vxId', String(length=30)),
    Column('pmLink', String(length=120)),
    Column('subDomain', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].columns['mdhLink'].drop()
    pre_meta.tables['amateur'].columns['vxLink'].drop()
    post_meta.tables['amateur'].columns['vxId'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].columns['mdhLink'].create()
    pre_meta.tables['amateur'].columns['vxLink'].create()
    post_meta.tables['amateur'].columns['vxId'].drop()

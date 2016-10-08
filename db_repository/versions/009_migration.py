from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateur = Table('amateur', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('twitter', VARCHAR(length=30)),
    Column('pmLink', VARCHAR(length=120)),
    Column('subDomain', VARCHAR(length=30)),
    Column('mdhId', VARCHAR(length=30)),
    Column('vxId', VARCHAR(length=30)),
    Column('mdhLink', VARCHAR(length=120)),
)

amateur = Table('amateur', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('tw', String(length=30)),
    Column('twDetail', Boolean),
    Column('mdhId', String(length=30)),
    Column('mdhDetail', Boolean),
    Column('vxId', String(length=30)),
    Column('vxDetail', Boolean),
    Column('pmId', String(length=120)),
    Column('pmDetail', Boolean),
    Column('subDomain', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].columns['mdhLink'].drop()
    pre_meta.tables['amateur'].columns['pmLink'].drop()
    pre_meta.tables['amateur'].columns['twitter'].drop()
    post_meta.tables['amateur'].columns['mdhDetail'].create()
    post_meta.tables['amateur'].columns['pmDetail'].create()
    post_meta.tables['amateur'].columns['pmId'].create()
    post_meta.tables['amateur'].columns['tw'].create()
    post_meta.tables['amateur'].columns['twDetail'].create()
    post_meta.tables['amateur'].columns['vxDetail'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].columns['mdhLink'].create()
    pre_meta.tables['amateur'].columns['pmLink'].create()
    pre_meta.tables['amateur'].columns['twitter'].create()
    post_meta.tables['amateur'].columns['mdhDetail'].drop()
    post_meta.tables['amateur'].columns['pmDetail'].drop()
    post_meta.tables['amateur'].columns['pmId'].drop()
    post_meta.tables['amateur'].columns['tw'].drop()
    post_meta.tables['amateur'].columns['twDetail'].drop()
    post_meta.tables['amateur'].columns['vxDetail'].drop()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateur = Table('amateur', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('tw', VARCHAR(length=15)),
    Column('twDetail', BOOLEAN),
    Column('mdhId', VARCHAR(length=30)),
    Column('mdhDetail', BOOLEAN),
    Column('vxId', VARCHAR(length=30)),
    Column('vxDetail', BOOLEAN),
    Column('pmId', VARCHAR(length=30)),
    Column('pmDetail', BOOLEAN),
    Column('subDomain', VARCHAR(length=30)),
)

amateure = Table('amateure', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('tw', String(length=15)),
    Column('twDetail', Boolean),
    Column('mdhId', String(length=30)),
    Column('mdhDetail', Boolean),
    Column('vxId', String(length=30)),
    Column('vxDetail', Boolean),
    Column('pmId', String(length=30)),
    Column('pmDetail', Boolean),
    Column('subDomain', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].drop()
    post_meta.tables['amateure'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateur'].create()
    post_meta.tables['amateure'].drop()

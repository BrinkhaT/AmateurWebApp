from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateure = Table('amateure', pre_meta,
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateure'].columns['mdhDetail'].drop()
    pre_meta.tables['amateure'].columns['pmDetail'].drop()
    pre_meta.tables['amateure'].columns['twDetail'].drop()
    pre_meta.tables['amateure'].columns['vxDetail'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['amateure'].columns['mdhDetail'].create()
    pre_meta.tables['amateure'].columns['pmDetail'].create()
    pre_meta.tables['amateure'].columns['twDetail'].create()
    pre_meta.tables['amateure'].columns['vxDetail'].create()

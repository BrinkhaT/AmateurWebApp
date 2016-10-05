from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
amateur = Table('amateur', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('twitter', String(length=30)),
    Column('mdhLink', String(length=120)),
    Column('vxLink', String(length=120)),
    Column('pmLink', String(length=120)),
    Column('subDomain', String(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amateur'].columns['mdhLink'].create()
    post_meta.tables['amateur'].columns['pmLink'].create()
    post_meta.tables['amateur'].columns['subDomain'].create()
    post_meta.tables['amateur'].columns['vxLink'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['amateur'].columns['mdhLink'].drop()
    post_meta.tables['amateur'].columns['pmLink'].drop()
    post_meta.tables['amateur'].columns['subDomain'].drop()
    post_meta.tables['amateur'].columns['vxLink'].drop()

from sqlalchemy import Table, Column, Integer, String, Date, Text, MetaData

metadata_obj = MetaData()

data_table = Table(
    "data",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('url', Text),
    Column('title', Text),
    Column('article', Text),
    Column('topic', Text),
    Column('tags', Text),
    Column('art_date', Date),
    Column('loc', Text)
)

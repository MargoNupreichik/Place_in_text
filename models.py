from sqlalchemy import Table, Column, Integer, String, Date, Text, MetaData
# from database import Base

# декларативный стиль

# class NewsOrm(Base):
#     __table__ = Table('data')
#     id = Column(Integer, primary_key=True)
#     url = Column(Text)
#     title = Column(Text)
#     article = Column(Text)
#     topic = Column(Text)
#     tags = Column(Text)
#     art_date = Column(Date)
#     loc = Column(Text)


# императивный стиль

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

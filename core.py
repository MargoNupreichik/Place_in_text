from models import metadata_obj
from database import engine
from sqlalchemy import insert, text

def create_tables():
    engine.echo = False
    metadata_obj.create_all(engine)
    engine.echo = True

def insert_data(data):
    with engine.connect() as conn:
        
        # классический метод (быстрее)
        # stmt = f"INSERT INTO data (url, title, article, topic, tags, art_date, loc) 
        #     VALUES {data['url']}, {data['title']}, {data['article']}, {data['topic']}, 
        #     {data['tags']}, {data['art_date'], {data['loc']}};"
        # conn.execute(text(stmt))
        
        # используя query builder (медленнее, но более предпочитетльный в силу читаемости)
        stmt = insert(data).values(
            url = data['url'],
            title = data['title'],
            article = data['article'],
            topic = data['topic'],
            tags = data['tags'],
            art_date = data['art_date'],
            loc = data['loc']
        )
        
        conn.execute(stmt)
        conn.commit()


from models import metadata_obj, data_table
from database import engine, session
from sqlalchemy import insert, select, text


class SyncCore:

    @staticmethod
    def create_tables():
        engine.echo = False
        metadata_obj.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_data(data):
        with engine.connect() as conn:
            stmt = insert(data).values(
                url=data['url'],
                title=data['title'],
                article=data['article'],
                topic=data['topic'],
                tags=data['tags'],
                art_date=data['art_date'],
                loc=data['loc']
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_to_html(left_data, right_data, order_by_loc=False):
        print(data_table)
        with engine.connect() as conn:
            if order_by_loc:
                query = select([data_table.c.id, data_table.c.art_date, data_table.c.loc, data_table.c.article]). \
                    where(data_table.c.art_date.between(left_data, right_data)). \
                    order_by(data_table.c.art_date.asc(), data_table.c.loc.asc())
            else:
                query = select([data_table.c.id, data_table.c.art_date, data_table.c.loc, data_table.c.article]). \
                    where(data_table.c.art_date.between(left_data, right_data)). \
                    order_by(data_table.c.art_date.asc())

            result = conn.execute(query)
            articles = result.all()
            return articles


class SyncORM:

    def select_data(left_data, right_data, order_by_loc=False):
        instance = NewsOrm()
        with session() as session:
            print('select')

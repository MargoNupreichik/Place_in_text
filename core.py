from models import metadata_obj, data_table
from database import engine
from sqlalchemy import insert, select, text


class SyncCore:

    """
    Класс SyncCore, описывающий интерфейс взаимодействия базы данных с приложением.

    Методы:
    create_tables() - создать новые таблицы;
    insert_data(data) - обработать данные data и вставить их в таблицу;
    select_to_html(left_date, right_date, order_by_loc=False) - создать запрос в базу, отобрать данные в диапазоне
    left_date (дата начала) - right_date (дата конца), отсортировать их по дате или по местоположению (в зависимости
    от значения order_by_loc) и вернуть результат в приложение.
    """

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
    def select_to_html(left_date, right_date, order_by_loc=False):
        print(data_table)
        with engine.connect() as conn:
            query = select([data_table.c.id, data_table.c.art_date, data_table.c.loc, data_table.c.article]). \
                    where(data_table.c.art_date.between(left_date, right_date)). \
                    order_by(text(f"{'loc asc, art_date asc' if order_by_loc else 'art_date asc'}"))

            result = conn.execute(query)
            articles = result.all()
            return articles

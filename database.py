import sqlalchemy
import sqlalchemy.orm
from local_settings import postgresql as settings


def get_engine(user, passwd, host, port, db) -> sqlalchemy.engine.Engine:

    """
    Функция get_engine, создающая движок для подключения к базе данных

    :param user: str
    :param passwd: str
    :param host: str
    :param port: str
    :param db: str
    :return: sqlalchemy.engine.Engine
    """

    url: str = 'postgresql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db
    # echo=True - все запросы будут дублироваться в консоль
    # pool_size=5, max_overflow=10 - ограничения по пулингу подключения
    engine: sqlalchemy.engine.Engine = sqlalchemy.create_engine(url, pool_size=5, echo=True, max_overflow=10)
    return engine


def get_engine_from_session() -> sqlalchemy.engine.Engine:

    """
    Функция get_engine_from_session, создающая движок для подключения к базе данных.
    Является оберткой для функции get_engine_from_session, в которой дополнительно берутся и проверяются данные о базе.

    :return: sqlalchemy.engine.Engine
    """

    keys = ['pguser', 'pgpassword', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file.')
    return get_engine(settings['pguser'], settings['pgpassword'], settings['pghost'],
                      settings['pgport'], settings['pgdb'])


engine: sqlalchemy.engine.Engine = get_engine_from_session()
session: sqlalchemy.orm.session = sqlalchemy.orm.sessionmaker(engine)


def tester() -> None:

    """
    Функция tester для тестирования подключения к базе данных.

    :return: None
    """

    with engine.connect() as conn:
        res = conn.execute(sqlalchemy.text("SELECT * FROM data LIMIT 5"))
        print(f"\n{res.first()=}")

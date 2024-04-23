
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from local_settings import postgresql as settings



def get_engine(user, passwd, host, port, db):
    # url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    url = 'postgresql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db
    engine = create_engine(url, pool_size=5, echo=True, max_overflow=10) # echo будет сыпать все запросы в консоль
                                                                         # max_overflow - доп. подключения
    return engine

def get_engine_from_session():
    keys = ['pguser', 'pgpassword', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file.')
    return get_engine(settings['pguser'], settings['pgpassword'], settings['pghost'], settings['pgport'], settings['pgdb'])

# !!!
engine = get_engine_from_session()
# !!!

session = sessionmaker(engine)

# class Base(DeclarativeBase):
#     pass

def tester():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM data LIMIT 5"))
        print()
        print(f"{res.first()=}")

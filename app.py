from flask import Flask, render_template

import psycopg2 
from flask_sqlalchemy import SQLAlchemy as alch
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from local_settings import postgresql as settings

app = Flask(__name__)

# декоратор - обработчик
# главная страница
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about") 
def about():
    return render_template('about.html')




# работа с DB
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

def get_session():
    engine = get_engine_from_session()
    session = sessionmaker(bind=engine)
    return session




# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    engine = get_engine_from_session()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))

    # app.run(debug=True)
    

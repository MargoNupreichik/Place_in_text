from flask import Flask, render_template

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import database
import core

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


# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    database.tester()
    # app.run(debug=True)
    

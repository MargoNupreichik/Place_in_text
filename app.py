from flask import Flask, render_template

import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import database
import core

from local_settings import postgresql as settings

app = Flask(__name__)

left = datetime.date(2000, 1, 1)
right = datetime.date(2000, 1, 10)


def prep_strings(string):
    return str(string[0]) + ' ' + string[1].strftime("%B %d, %Y") + " " + string[2]

# декоратор - обработчик
# главная страница
@app.route("/index")
@app.route("/")
def index():
    strings = core.SyncCore.select_to_html(left, right)
    strings_ = []
    for st in strings:
        strings_.append(prep_strings(st))
    return render_template('index.html', strings=strings_)

@app.route("/about") 
def about():
    return render_template('about.html')


# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    # database.tester()
    app.run(debug=True)
    

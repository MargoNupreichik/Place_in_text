from flask import Flask, render_template, request, redirect, url_for

import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import database
import core

from local_settings import postgresql as settings

app = Flask(__name__)

left = datetime.date(2000, 1, 1)
right = datetime.date(2000, 1, 10)
order = "cheked"


def prep_strings(string):
    return string[1].strftime("%B %d, %Y") + " " + string[2]

def prep_texts(string):
    return str(string[3])

# декоратор - обработчик
# главная страница
@app.route("/index")
@app.route("/")
def index():
    strings = core.SyncCore.select_to_html(left, right)
    strings_ = []
    articles_ = []
    for st in strings:
        strings_.append(prep_strings(st))
        articles_.append(prep_texts(st))
    return render_template('index.html', strings=strings_, articles=articles_, l_d=left, r_d=right, order=order)

@app.route("/about") 
def about():
    return render_template('about.html')


@app.route('/process_data/', methods=['GET', 'POST'])
def updating():
    data = request.form['data']
    print(data)
    left_, right_, order = data.split('/')
    print(left_, right_)
    global left 
    left = datetime.datetime.strptime(left_, '%Y-%m-%d').date()
    global right 
    right = datetime.datetime.strptime(right_, '%Y-%m-%d').date()
    return redirect(url_for('index'))   

# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    # database.tester()
    app.run(debug=True)
    

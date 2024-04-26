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
order = "cheсked"


def prep_strings(string):
    return string[1].strftime("%B %d, %Y") + " " + string[2]

def prep_texts(string):
    return str(string[3])

def prep_places(string):
    return str(string[2])

# декоратор - обработчик
# главная страница
@app.route("/index")
@app.route("/")
def index():
    global order
    order_l = True if order == "true" else False
    strings = core.SyncCore.select_to_html(left, right, order_by_loc=order_l)
    strings_ = []
    places_ = []
    articles_ = []
    geo_=[]
    for st in strings:
        st_ = prep_strings(st)
        st_loc = list(st_.split(' '))[-1]
        strings_.append(st_)
        articles_.append(prep_texts(st))
        places_.append(st_loc)
    print(places_[0])
    return render_template('index.html', strings=strings_, articles=articles_, 
                           l_d=left, r_d=right, order_loc=order_l,
                           places=places_)

@app.route("/about") 
def about():
    return render_template('about.html')


@app.route('/process_data/', methods=['GET', 'POST'])
def updating():
    data = request.form['data']
    print(data)
    left_, right_, order_ = data.split('/')
    print(left_, right_)
    global left 
    left = datetime.datetime.strptime(left_, '%Y-%m-%d').date()
    global right 
    right = datetime.datetime.strptime(right_, '%Y-%m-%d').date()
    print('-----------------------------------------------')
    print(order_)
    global order
    order = order_
    print('----------------------------------------------------------------')
    print(order, order_, sep='<---')
    return redirect(url_for('index'))   

# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    # database.tester()
    app.run(debug=True)
    

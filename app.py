import flask
import datetime
import werkzeug
import core

app = flask.app.Flask(__name__)

left = datetime.date(2000, 1, 1)
right = datetime.date(2000, 1, 10)
order = "cheсked"


def prep_strings(string) -> str:
    """
    Функция-обработчик prep_strings.
    Склеивает поля "дата" и "локация" и возвращает полученную строку.

    :param string: object
    :return: str
    """

    return string[1].strftime("%B %d, %Y") + " " + string[2]


def prep_texts(string) -> str:
    """
    Функция-обработчик prep_texts.
    Преобразует поле "текст статьи" в строковый тип и возвращает результат.

    :param string: object
    :return: str
    """

    return str(string[3])


@app.route("/index")
@app.route("/")
def index() -> str:
    """
    Обработчик страниц / и /index (основные страницы приложения).
    Подтягивает данные с базы данных по запросу пользователя и вовзвращает их обратно в приложение.

    :return: str
    """

    global order
    order_l = True if order == "true" else False
    strings = core.SyncCore.select_to_html(left, right, order_by_loc=order_l)
    strings_ = []
    places_ = []
    articles_ = []
    for st in strings:
        st_ = prep_strings(st)
        st_loc = ' '.join(st_.split(' ')[3:])
        strings_.append(st_)
        articles_.append(prep_texts(st))
        places_.append(st_loc)
    print(places_[0])
    return flask.render_template('index.html', strings=strings_, articles=articles_,
                                 l_d=left, r_d=right, order_loc=order_l, places=places_)


@app.route("/about")
def about() -> str:
    """
    Обработчик страницы /about ("О проекте").

    :return: str
    """

    return flask.render_template('about.html')


@app.route('/process_data/', methods=['GET', 'POST'])
def updating() -> werkzeug.Response:
    """
    Обработчик страницы /process_data/ (вызывается при нажатии кнопки "Поиск").
    Меняет значения на полученные с приложения и обновляет главную страницу.

    :return: werkzeug.Response
    """

    global order, left, right
    data: str = flask.request.form['data']
    print(data)
    left_, right_, order_ = data.split('/')
    print(left_, right_)
    left = datetime.datetime.strptime(left_, '%Y-%m-%d').date()
    right = datetime.datetime.strptime(right_, '%Y-%m-%d').date()
    print('-----------------------------------------------')
    print(order_)
    order = order_
    print('----------------------------------------------------------------')
    print(order, order_, sep='<---')
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    """
    Точка входа в приложение.
    
    Для теста базы данных перед запуском приложения можно написать database.tester()
    
    Для перевода приложения в режим отладки добавить необязательный аргумент:
    app.run() -> app.run(debug=True)
    
    Режим отладки отображает исключения вместо страницы с кодом 500 и позволяет настраивать любую часть приложения
    на ходу.
    """

    app.run(debug=True)

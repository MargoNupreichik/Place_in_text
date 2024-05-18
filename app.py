import flask
import datetime
import werkzeug
import core
import requests

app = flask.app.Flask(__name__)

left = datetime.date(2014, 3, 16)
right = datetime.date(2014, 3, 18)
order = "checked"
strings_ = []
places_ = []
articles_ = []
coords_ = []


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
    global order, strings_, places_, articles_, coords_
    order_l = True if order == "true" else False
    if len(strings_) == 0:  # если данных еще не было загружено в систему, нужно загрузить их с базы данных
        strings = core.SyncCore.select_to_html(left, right, order_by_loc=order_l)
        for st in strings:
            st_ = prep_strings(st)
            st_loc = ' '.join(st_.split(' ')[3:])
            req = requests.get(f"https://nominatim.openstreetmap.org/search",
                               headers={'Accept': 'application/json', 'User-Agent': 'Modeler'},
                               params={'q': st_loc, 'format': 'json'}).json()
            if req:
                strings_.append(st_)
                articles_.append(prep_texts(st))
                places_.append(st_loc)
                coords_.append([float(req[0]['lat']), float(req[0]['lon'])])
    print(places_[0])
    return flask.render_template('index.html', strings=strings_, articles=articles_,
                                 l_d=left, r_d=right, order_loc=order_l, places=places_, coords=coords_)


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

    global order, left, right, strings_, places_, articles_, coords_
    data: str = flask.request.form['data']
    print(data)
    left_, right_, order_ = data.split('/')
    print(left_, right_)
    left_ = datetime.datetime.strptime(left_, '%Y-%m-%d').date()
    right_ = datetime.datetime.strptime(right_, '%Y-%m-%d').date()
    if left_ != left or right_ != right:
        strings_ = []
        places_ = []
        articles_ = []
        coords_ = []
    left = left_
    right = right_
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

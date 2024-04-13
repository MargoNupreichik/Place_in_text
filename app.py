from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy as alch

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

# работа с DB Postgres
# engine = alch.create_engine("postgresql+psycopg2://root:pass@localhost/mydb")


# файл основной для данного приложения
if __name__ == '__main__':
    # debug = True нужно чтобы сервер автоматически перезапускался
    # не нужно перезапускать программу - обновили в браузере и все
    app.run(debug=True)
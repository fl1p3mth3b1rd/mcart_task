from flask import Flask, request
import methods
import json

app = Flask(__name__)

@app.route("/")
def index():
    if request.method == 'GET':
        # получение списка валют
        if request.args.get("method") == "get_curriencies":
            print(methods.get_curriencies())
            curriencies_dict = json.dumps(methods.get_curriencies(), ensure_ascii=False)
            return f"список кодов валют:\n {curriencies_dict}"
        if request.args.get("method") == "get_exchange_rate":
        # получение информации о курсе валюты (char_code) относительно рубля по заданным датам (first_date, second_date) и разность между полученными значениями
            if request.args.get("char_code") and request.args.get("first_date") and request.args.get("second_date"):
                return methods.get_exchange_rate(request.args.get("char_code"), request.args.get("first_date"), request.args.get("second_date"))
            else:
                return "Отсутсвует один или несколько параметров из следующего списка: char_code, first_date, second_date"
    # стартовая страница
    return """<h1>API для получения курсов валют по двум датам и их разности<h1>
            <h2>Методы:</h2>
            <h3>1) GET-запрос с параметрами: method=get_curriencies - позволяет получить список валют</h3>
            <h3>2) GET-запрос с параметрами: method=get_exchange_rate, char_code (строка) - код валюты, 
            first_date (строка) - первая дата (формат: YYYY.mm.dd), 
            second_date (строка) - вторая дата (формат: YYYY.mm.dd) - 
            позволяет получить информацию о разнице в курсе валют между указанными датами</h3>
            <p>пример GET-запроса: http://127.0.0.1:5000/?method=get_exchange_rate&char_code=GBP&first_date=2021.08.19&second_date=2021.08.20</p>
            <p><a href=http://127.0.0.1:5000/?method=get_exchange_rate&char_code=GBP&first_date=2021.08.19&second_date=2021.08.20>пример ответа</a></p>"""

if __name__=="__main__":
    app.run()
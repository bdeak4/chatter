from bottle import route, run, template

from data import fetch_data_in_background


@route("/")
def index():
    return template("idx")


@route("/data")
def data():
    return template("data")


fetch_data_in_background()
run(host="localhost", port=8080)

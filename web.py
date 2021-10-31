#!venv/bin/python

from bottle import route, run, template
import sqlite3
import pathlib

from data import fetch_data_in_background

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()


@route("/")
def index():
    processed_today_count = cur.execute(
        pathlib.Path("queries/processed_today.sql").read_text()
    ).fetchone()[0]
    return template(
        "index.html",
        processed_today_count=processed_today_count,
    )


fetch_data_in_background()
run(host="0.0.0.0", port=8080, server="waitress")

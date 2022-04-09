#!venv/bin/python

from bottle import route, run, template, static_file
import sqlite3
import datetime

import statistics
import ingestion
import database


@route("/")
def index():
    with sqlite3.connect("chatter.db") as con:
        return template(
            "index.html",
            mention_growth_coins=statistics.mention_growth_coins_by_time_period(con),
            total_charts=statistics.total_charts(con),
            weekly_count=statistics.weekly_count_by_content_type(con),
            current_year=datetime.date.today().year,
        )


@route("/static/<filepath:path>")
def static(filepath):
    return static_file(filepath, root="static")


database.init()
ingestion.ingest_in_background()
run(host="0.0.0.0", port=8080, server="waitress")

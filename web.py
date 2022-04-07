#!venv/bin/python

from bottle import route, run, template, static_file
import sqlite3
import datetime

import statistics
import ingestion


@route("/")
def index():
    with sqlite3.connect("chatter.db") as con:
        return template(
            "index.html",
            total_mentions=statistics.total_mentions_by_time_period(con),
            total_market_cap=statistics.total_market_cap_by_time_period(),
            weekly_count=statistics.weekly_count_by_content_type(con),
            current_year=datetime.date.today().year,
        )


@route("/static/<filepath:path>")
def static(filepath):
    return static_file(filepath, root="static")


ingestion.ingest_in_background()

run(host="0.0.0.0", port=8080, server="waitress")

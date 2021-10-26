#!venv/bin/python

from bottle import route, run, template

from data import fetch_data_in_background
from stats import *


@route("/")
def index():
    return "chatter"
    # return template(
    #    "index.html",
    #    top_week_growth=get_top_week_growth(),
    #    processed_today_count=get_processed_today_count(),
    # )


fetch_data_in_background()
run(host="0.0.0.0", port=8080, server="waitress")

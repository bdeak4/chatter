from flask import Flask, render_template
import os
import datetime

import database
import statistics
import wsgi


app = Flask(__name__)


@app.route("/")
def index():
    with database.get_conn() as conn:
        stats = statistics.get_statistics_data(conn)
        return render_template(
            "index.jinja",
            mention_growth_coins=stats["mention_growth_coins"],
            total_charts=stats["total_charts"],
            weekly_count=stats["weekly_count"],
            current_year=datetime.date.today().year,
        )


@app.before_first_request
def setup():
    if os.getenv("FLASK_ENV") == "development":
        wsgi.on_starting(None)
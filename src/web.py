from flask import Flask, render_template
import os
import datetime

import stats
import wsgi


app = Flask(__name__)


@app.route("/")
def index():
    statistics = stats.get_statistics_data()
    return render_template(
        "index.jinja",
        mention_growth_coins=statistics["mention_growth_coins"],
        total_charts=statistics["total_charts"],
        weekly_count=statistics["weekly_count"],
        current_year=datetime.date.today().year,
    )


@app.before_first_request
def setup():
    if os.getenv("FLASK_ENV") == "development":
        wsgi.on_starting(None)

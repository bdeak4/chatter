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
        return render_template(
            "index.jinja",
            mention_growth_coins=statistics.mention_growth_coins_by_time_period(conn),
            total_charts=statistics.total_charts(conn),
            weekly_count=statistics.weekly_count_by_content_type(conn),
            current_year=datetime.date.today().year,
        )


@app.before_first_request
def setup():
    if os.getenv("FLASK_ENV") == "development":
        wsgi.on_starting(None)
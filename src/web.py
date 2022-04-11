from flask import Flask, render_template
import sqlite3
import datetime

import statistics
import ingestion
import database

app = Flask(__name__)

@app.route("/")
def index():
    with sqlite3.connect("../chatter.db") as con:
        return render_template(
            "index.jinja",
            mention_growth_coins=statistics.mention_growth_coins_by_time_period(con),
            total_charts=statistics.total_charts(con),
            weekly_count=statistics.weekly_count_by_content_type(con),
            current_year=datetime.date.today().year,
        )


database.init()
ingestion.ingest_in_background()
from flask import Flask, render_template
import psycopg2
import os
import datetime

import statistics
import ingestion
import coingecko

app = Flask(__name__)


@app.route("/")
def index():
    with psycopg2.connect(os.getenv("POSTGRES_URL")) as conn:
        return render_template(
            "index.jinja",
            mention_growth_coins=statistics.mention_growth_coins_by_time_period(conn),
            total_charts=statistics.total_charts(conn),
            weekly_count=statistics.weekly_count_by_content_type(conn),
            current_year=datetime.date.today().year,
        )


ingestion.ingest_in_background()
coingecko.cache_warm_up()
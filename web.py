#!venv/bin/python

from bottle import route, run, template, static_file
import sqlite3
import datetime

import statistics
import ingestion


con = sqlite3.connect("chatter.db")


def db_init():
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mentions (
            symbol, timestamp, content_type, polarity, subjectivity
        );
        """
    )
    cur.execute(
        """
        CREATE VIEW IF NOT EXISTS mention_stats AS
        SELECT *,
            1.0 * total / LAG(total) OVER (PARTITION BY symbol ORDER BY date) AS growth
        FROM (
            SELECT symbol,
                DATE(timestamp) AS date,
                COUNT(CASE WHEN polarity > 0 THEN 1 END)              AS pol_positive,
                COUNT(CASE polarity WHEN 0 THEN 1 END)                AS pol_neutral,
                COUNT(CASE WHEN polarity < 0 THEN 1 END)              AS pol_negative,
                COUNT(CASE WHEN subjectivity >= 0.5 THEN 1 END)       AS sub_subjective,
                COUNT(CASE WHEN subjectivity < 0.5 THEN 1 END)        AS sub_objective,
                COUNT(CASE content_type WHEN "submission" THEN 1 END) AS ct_submission,
                COUNT(CASE content_type WHEN "comment" THEN 1 END)    AS ct_comment,
                COUNT(*) AS total
            FROM mentions
            GROUP BY symbol, date
        )
        """
    )
    con.commit()


@route("/")
def index():
    return template(
        "index.html",
        total_mentions=statistics.total_mentions_by_time_period(con),
        total_market_cap=statistics.total_market_cap_by_time_period(),
        btc_price=statistics.btc_price_by_time_period(),
        weekly_count=statistics.weekly_count_by_content_type(con),
        current_year=datetime.date.today().year,
    )


@route("/static/<filepath:path>")
def static(filepath):
    return static_file(filepath, root="static")


db_init()
ingestion.ingest_in_background()
run(host="0.0.0.0", port=8080, server="waitress")

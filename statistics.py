import helpers
from datetime import date
import requests

from ingestion import get_coingecko_market_cap_data


def total_mentions_by_time_period(con):
    return {
        "week": map(str, total_mentions(con, "week")),
        "month": map(str, total_mentions(con, "month")),
        "quarter": map(str, total_mentions(con, "quarter")),
        "year": map(str, total_mentions(con, "year")),
    }


def total_mentions(con, time_period):
    cur = con.cursor()
    cur.execute(
        """
        SELECT DATE(timestamp), COUNT(*)
        FROM mentions
        WHERE timestamp >= DATETIME('now', 'start of day', ?)
        GROUP BY DATE(timestamp);
        """,
        (helpers.sql_time_interval(time_period),),
    )
    mentions_by_date = helpers.fill_blanks(time_period, cur.fetchall())
    return list(map(lambda m: m[1], mentions_by_date))


def total_market_cap_by_time_period():
    return {
        "week": map(str, total_market_cap("week")),
        "month": map(str, total_market_cap("month")),
        "quarter": map(str, total_market_cap("quarter")),
        "year": map(str, total_market_cap("year")),
    }


def total_market_cap(time_period):
    number_of_data_points = helpers.time_period_len(time_period)
    market_cap_by_date = get_coingecko_market_cap_data()[-number_of_data_points:]
    return list(map(lambda d: int(d[1]), market_cap_by_date))


def weekly_count_by_content_type(con):
    return {
        "submission": count(con, "week", "submission"),
        "comment": count(con, "week", "comment"),
    }


def count(con, time_period, content_type):
    cur = con.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM mentions
        WHERE timestamp >= DATETIME('now', 'start of day', ?)
          AND content_type = ?;
        """,
        (helpers.sql_time_interval(time_period), content_type),
    )
    return cur.fetchone()[0]

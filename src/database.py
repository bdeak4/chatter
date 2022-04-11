import sqlite3
import helpers


def init():
    with sqlite3.connect("../chatter.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS mentions (
                symbol, timestamp, content_type, polarity, subjectivity
            );
            """
        )
        cur.execute(get_stats_view("day", "week"))
        cur.execute(get_stats_view("week", "month"))
        cur.execute(get_stats_view("month", "year"))
        con.commit()


def get_stats_view(time_increments, time_period):
    return f"""
        CREATE VIEW IF NOT EXISTS mention_stats_by_{time_increments} AS
        SELECT *,
            1.0 * total / LAG(total) OVER (PARTITION BY symbol ORDER BY time_period) AS growth
        FROM (
            SELECT symbol,
                {helpers.sql_time_period_from_ts(time_increments)}    AS time_period,
                COUNT(CASE WHEN polarity > 0 THEN 1 END)              AS pol_positive,
                COUNT(CASE polarity WHEN 0 THEN 1 END)                AS pol_neutral,
                COUNT(CASE WHEN polarity < 0 THEN 1 END)              AS pol_negative,
                COUNT(CASE WHEN subjectivity >= 0.5 THEN 1 END)       AS sub_subjective,
                COUNT(CASE WHEN subjectivity < 0.5 THEN 1 END)        AS sub_objective,
                COUNT(CASE content_type WHEN "submission" THEN 1 END) AS ct_submission,
                COUNT(CASE content_type WHEN "comment" THEN 1 END)    AS ct_comment,
                COUNT(*)                                              AS total
            FROM mentions
            WHERE timestamp >= DATETIME('now', 'start of day', '{helpers.sql_time_interval(time_period)}')
            GROUP BY symbol, time_period
        )
    """

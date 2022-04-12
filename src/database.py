import psycopg2
import os
import helpers


def init():
    with psycopg2.connect(os.getenv("POSTGRES_URL")) as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS mentions (
                symbol VARCHAR(10),
                timestamp TIMESTAMP,
                content_type VARCHAR(10),
                polarity REAL,
                subjectivity REAL
            );
            """
        )
        cur.execute(get_stats_view("day", "week"))
        cur.execute(get_stats_view("week", "month"))
        cur.execute(get_stats_view("month", "year"))
        con.commit()


def get_stats_view(time_increments, time_period):
    return f"""
        CREATE OR REPLACE VIEW mention_stats_by_{time_increments} AS
        SELECT *,
            1.0 * total / LAG(total) OVER (PARTITION BY symbol ORDER BY time_period) AS growth
        FROM (
            SELECT symbol,
                {helpers.sql_time_period_from_ts(time_increments)}      AS time_period,
                COUNT(CASE WHEN polarity > 0                THEN 1 END) AS pol_positive,
                COUNT(CASE WHEN polarity = 0                THEN 1 END) AS pol_neutral,
                COUNT(CASE WHEN polarity < 0                THEN 1 END) AS pol_negative,
                COUNT(CASE WHEN subjectivity >= 0.5         THEN 1 END) AS sub_subjective,
                COUNT(CASE WHEN subjectivity < 0.5          THEN 1 END) AS sub_objective,
                COUNT(CASE WHEN content_type = 'submission' THEN 1 END) AS ct_submission,
                COUNT(CASE WHEN content_type = 'comment'    THEN 1 END) AS ct_comment,
                COUNT(*)                                                AS total
            FROM mentions
            WHERE timestamp >= NOW() - INTERVAL '{helpers.sql_time_interval(time_period)}'
            GROUP BY symbol, time_period
        ) AS mentions
    """

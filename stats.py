import sqlite3

con = sqlite3.connect("data.db")


def get_processed_today_count():
    cur = con.cursor()
    return cur.execute(
        """
        SELECT SUM(count)
        FROM tickers
        WHERE date = DATE();
        """
    ).fetchone()[0]


def get_top_week_growth():
    cur = con.cursor()
    tickers = cur.execute(
        """
        SELECT ticker, 100 * SUM(count) / MAX(SUM(count)) OVER() / 4 +
            100 * (
                SELECT SUM(count)
                FROM tickers
                WHERE ticker = t.ticker AND date >= DATE("now", "-7 days")
            ) / SUM(count) AS score
        FROM tickers t
        GROUP BY ticker
        ORDER BY score DESC
        LIMIT 5;
        """
    ).fetchall()
    results = []
    for ticker, score in tickers:
        points = cur.execute(
            """
            SELECT 100 * (SUM(count) - LAG(SUM(count), 1) OVER (ORDER BY date)) /
                LAG(SUM(count), 1) OVER (ORDER BY date) AS percent_change
            FROM tickers
            WHERE ticker = ? AND date >= DATE("now", "-7 days")
            GROUP BY date, ticker
            ORDER BY date;
            """,
            (ticker,),
        ).fetchall()
        results.append(
            {
                "ticker": ticker,
                "score": score,
                "points": [p[0] for p in points[1:]],
            }
        )
    return results


def get_most_talked_about_details():
    print("hi")


# SELECT ticker, SUM(count) AS count_agg FROM tickers WHERE date >= DATE("now", "-6 days") GROUP BY ticker ORDER BY count_agg DESC LIMIT 5;
# SELECT ticker, date, SUM(count) AS count, 100 * SUM(count) / LAG(count, 1) OVER (ORDER BY date ASC) AS growth FROM tickers WHERE ticker = 'ADA' GROUP BY date ORDER BY date ASC;

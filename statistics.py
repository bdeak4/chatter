from datetime import date

import helpers
import ingestion


def mention_growth_coins_by_time_period(con):
    return [
        ("past week", mention_growth_coins(con, "day", "week")),
        ("past month", mention_growth_coins(con, "week", "month")),
        ("coingecko trending", trending_coins(con)),
    ]


def mention_growth_coins(con, time_increment, time_period):
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT symbol, AVG(growth) AS avg_growth
        FROM mention_stats_by_{time_increment}
        GROUP BY symbol
        ORDER BY avg_growth DESC
        LIMIT 7;
        """
    )

    return list(map(lambda c: get_coin_data(con, c[0], time_period), cur.fetchall()))


def trending_coins(con):
    return list(
        map(
            lambda tc: get_coin_data(con, tc["item"]["symbol"], "week"),
            ingestion.get_coingecko_trending_data(),
        )
    )


def get_coin_data(con, symbol, time_period):
    cur = con.cursor()
    cur.execute(
        f"""
        SELECT pol_positive, pol_neutral, pol_negative,
            sub_subjective, sub_objective,
            ct_submission, ct_comment
        FROM mention_stats_by_{time_period}
        WHERE symbol = ?
        ORDER BY time_period DESC
        LIMIT 1;
        """,
        (symbol,),
    )
    data = cur.fetchone()
    if data == None:
        data = (0, 0, 0, 0, 0, 0, 0)

    cur.execute(
        """
        SELECT DATE(timestamp), COUNT(*)
        FROM mentions
        WHERE timestamp >= DATETIME('now', 'start of day', ?)
          AND symbol = ?
        GROUP BY DATE(timestamp);
        """,
        (helpers.sql_time_interval(time_period), symbol),
    )
    mentions_by_date = helpers.fill_blanks(time_period, cur.fetchall())

    return {
        "symbol": symbol,
        "pol_positive": data[0],
        "pol_neutral": data[1],
        "pol_negative": data[2],
        "sub_subjective": data[3],
        "sub_objective": data[4],
        "ct_submission": data[5],
        "ct_comment": data[6],
        "mentions": map(lambda m: str(m[1]), mentions_by_date),
        "price": map(str, get_price_by_symbol_and_time_period(symbol, time_period)),
        "url": "https://www.coingecko.com/en/coins/"
        + ingestion.get_coingecko_coin_data_by_symbol(symbol)["id"],
    }


def total_charts(con):
    return [
        ("total mentions", total_mentions_by_time_period(con)),
        ("total market cap", total_market_cap_by_time_period()),
        ("btc price", btc_price_by_time_period()),
    ]


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
    market_cap_by_date = ingestion.get_coingecko_market_cap_data()[
        -number_of_data_points:
    ]
    return list(map(lambda d: int(d[1]), market_cap_by_date))


def btc_price_by_time_period():
    return {
        "week": map(str, get_price_by_symbol_and_time_period("BTC", "week")),
        "month": map(str, get_price_by_symbol_and_time_period("BTC", "month")),
        "quarter": map(str, get_price_by_symbol_and_time_period("BTC", "quarter")),
        "year": map(str, get_price_by_symbol_and_time_period("BTC", "year")),
    }


def get_price_by_symbol_and_time_period(symbol, time_period):
    number_of_data_points = helpers.time_period_len(time_period)
    price_by_data_point = ingestion.get_coingecko_price_data_by_symbol(symbol)[
        -number_of_data_points:
    ]
    return list(map(lambda d: float(d[1]), price_by_data_point))


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

import helpers
import coingecko


def mention_growth_coins_by_time_period(conn):
    return [
        ("past week", mention_growth_coins(conn, "day", "week")),
        ("past month", mention_growth_coins(conn, "week", "month")),
        ("coingecko trending", trending_coins(conn)),
    ]


def mention_growth_coins(conn, time_increment, time_period):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT symbol, AVG(growth) AS avg_growth
        FROM mention_stats_by_{time_increment}
        GROUP BY symbol
        ORDER BY avg_growth DESC NULLS LAST
        LIMIT 7;
        """
    )

    return list(map(lambda c: get_coin_data(conn, c[0], time_period), cur.fetchall()))


def trending_coins(conn):
    return list(
        map(
            lambda tc: get_coin_data(conn, tc["item"]["symbol"], "week"),
            coingecko.get_coingecko_trending_data(),
        )
    )


def get_coin_data(conn, symbol, time_period):
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT pol_positive, pol_neutral, pol_negative,
            sub_subjective, sub_objective,
            ct_submission, ct_comment
        FROM mention_stats_by_{time_period}
        WHERE symbol = %s
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
        SELECT timestamp::DATE, COUNT(*)
        FROM mentions
        WHERE timestamp >= NOW() - INTERVAL %s
          AND symbol = %s
        GROUP BY timestamp::DATE;
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
        + coingecko.get_coingecko_coin_data_by_symbol(symbol)["id"],
    }


def total_charts(conn):
    return [
        ("total mentions", total_mentions_by_time_period(conn)),
        ("total market cap", total_market_cap_by_time_period()),
        ("btc price", btc_price_by_time_period()),
    ]


def total_mentions_by_time_period(conn):
    return {
        "week": map(str, total_mentions(conn, "week")),
        "month": map(str, total_mentions(conn, "month")),
        "quarter": map(str, total_mentions(conn, "quarter")),
        "year": map(str, total_mentions(conn, "year")),
    }


def total_mentions(conn, time_period):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT timestamp::DATE, COUNT(*)
        FROM mentions
        WHERE timestamp >= NOW() - INTERVAL %s
        GROUP BY timestamp::DATE;
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
    market_cap_by_date = coingecko.get_coingecko_market_cap_data()[
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
    price_by_data_point = coingecko.get_coingecko_price_data_by_symbol(symbol)[
        -number_of_data_points:
    ]
    return list(map(lambda d: float(d[1]), price_by_data_point))


def weekly_count_by_content_type(conn):
    return {
        "submission": count(conn, "week", "submission"),
        "comment": count(conn, "week", "comment"),
    }


def count(conn, time_period, content_type):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*)
        FROM mentions
        WHERE timestamp >= NOW() - INTERVAL %s
          AND content_type = %s;
        """,
        (helpers.sql_time_interval(time_period), content_type),
    )
    return cur.fetchone()[0]

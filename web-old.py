#!venv/bin/python

from bottle import route, run, template
import sqlite3
import pathlib
import datetime
import requests

from data import fetch_data_in_background

con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()


@route("/")
def index():
    crypto_rising_this_week = []
    for ticker in cur.execute(
        pathlib.Path("queries/rising_this_week.sql").read_text(), ("crypto",)
    ).fetchall():
        crypto_rising_this_week.append(process_ticker(ticker))

    stocks_rising_this_week = []
    for ticker in cur.execute(
        pathlib.Path("queries/rising_this_week.sql").read_text(), ("stock",)
    ).fetchall():
        stocks_rising_this_week.append(process_ticker(ticker))

    processed_today_count = cur.execute(
        pathlib.Path("queries/processed_today.sql").read_text()
    ).fetchone()[0]

    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    n = datetime.datetime.today().weekday() + 1
    weekdays = weekdays[n:] + weekdays[:n]
    weekdays = "".join(map(lambda x: f"&nbsp;{x}&nbsp;", weekdays))

    return template(
        "index.html",
        processed_today_count=processed_today_count,
        crypto_rising_this_week=crypto_rising_this_week,
        stocks_rising_this_week=stocks_rising_this_week,
        weekdays=weekdays,
    )


def process_ticker(ticker):
    count = ticker[7] + ticker[8]

    percent_change_by_day = ticker[9].split(",")
    days_with_change = ticker[10].split(",")
    change_by_day = []
    for i in range(6, -1, -1):
        if str(i) in days_with_change:
            n = percent_change_by_day[days_with_change.index(str(i))]
            change_by_day.append(
                '<span style="color: %s">%s%s%%</span>'
                % (
                    "green" if int(n) > 0 else "red",
                    (3 - len(str(n))) * "&nbsp;",
                    n if int(n) < 1000 else "999",
                )
            )
        else:
            change_by_day.append(4 * "&nbsp;")

    return {
        "name": ticker[0],
        "link": get_link(ticker[0], ticker[1]),
        "polarity_positive_count": get_percent(ticker[2], count),
        "polarity_neutral_count": get_percent(ticker[3], count),
        "polarity_negative_count": get_percent(ticker[4], count),
        "subjectivity_subjective_count": get_percent(ticker[5], count),
        "subjectivity_objective_count": get_percent(ticker[6], count),
        "source_post_count": get_percent(ticker[7], count),
        "source_comment_count": get_percent(ticker[8], count),
        "count": count,
        "score": str(round(ticker[11], 10)).ljust(12, "0"),
        "change_by_day": " ".join(change_by_day),
    }


def get_percent(a, b):
    s = str(round(a / b * 100))
    padding = (2 - len(s)) * "&nbsp;"
    return padding + s + "%"


crypto_links = {}
crypto_links_last_modified = 0


def get_link(ticker, type_):
    if type_ == "crypto":
        global crypto_links_last_modified
        today = datetime.datetime.now().day
        if crypto_links_last_modified != today:
            try:
                r = requests.get("https://api.coingecko.com/api/v3/search")
                crypto_links.clear()
                for coin in r.json()["coins"]:
                    if coin["symbol"] not in crypto_links:
                        crypto_links[coin["symbol"]] = coin["id"]
                crypto_links_last_modified = today
            except:
                pass
        if ticker in crypto_links:
            return (
                "https://www.coingecko.com/en/coins/%s" % crypto_links[ticker]
            )
    if type_ == "stock":
        return "https://finviz.com/quote.ashx?t=%s" % ticker
    return ""


fetch_data_in_background()
run(host="0.0.0.0", port=8080, server="waitress")

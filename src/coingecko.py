import requests
import json
from datetime import datetime, timedelta
import multiprocessing

config = json.loads(open("../config.json").read())


def is_on_coingecko(symbol):
    return (
        get_coingecko_coin_data_by_symbol(symbol) != None
        and not symbol in config["symbol_blocklist"]
    )


def get_coingecko_coin_data_by_symbol(symbol):
    for coin in get_coingecko_coin_data():
        if coin["symbol"] == symbol and coin["market_cap_rank"]:
            return coin

    return None


_coingecko_coin_data = []
_coingecko_coin_data_modified = datetime(2009, 1, 9)


def get_coingecko_coin_data():
    if (datetime.now() - _coingecko_coin_data_modified) > timedelta(hours=6):
        try_bg(_update_coingecko_coin_data, _coingecko_coin_data_modified)

    return _coingecko_coin_data


def _update_coingecko_coin_data():
    global _coingecko_coin_data
    global _coingecko_coin_data_modified

    r = requests.get("https://api.coingecko.com/api/v3/search")
    if r.ok:
        _coingecko_coin_data = r.json()["coins"]
        _coingecko_coin_data_modified = datetime.now()


_coingecko_market_cap_data = []
_coingecko_market_cap_data_modified = datetime(2009, 1, 9)


def get_coingecko_market_cap_data():
    if (datetime.now() - _coingecko_market_cap_data_modified) > timedelta(hours=6):
        _update_coingecko_market_cap_data()
        try_bg(_update_coingecko_market_cap_data, _coingecko_market_cap_data_modified)

    return _coingecko_market_cap_data


def _update_coingecko_market_cap_data():
    global _coingecko_market_cap_data
    global _coingecko_market_cap_data_modified

    r = requests.get(
        "https://www.coingecko.com/market_cap/total_charts_data?vs_currency=usd"
    )
    if r.ok:
        _coingecko_market_cap_data = r.json()["stats"]
        _coingecko_market_cap_data_modified = datetime.now()


_coingecko_price_data = {}


def get_coingecko_price_data_by_symbol(symbol):
    if symbol not in _coingecko_price_data or (
        datetime.now() - _coingecko_price_data[symbol]["modified"]
    ) > timedelta(hours=2):
        try_bg(
            _update_coingecko_price_data_by_symbol,
            _coingecko_price_data[symbol]["modified"]
            if symbol in _coingecko_price_data
            else datetime(2009, 1, 9),
            args=(symbol,),
        )

    return _coingecko_price_data[symbol]["prices"]


def _update_coingecko_price_data_by_symbol(symbol):
    global _coingecko_price_data

    coin = get_coingecko_coin_data_by_symbol(symbol)
    if coin == None:
        _coingecko_price_data[symbol] = {"prices": [], "modified": datetime.now()}
        return

    days = 366 if symbol == "BTC" else 32  # btc needs year of price data for chart
    r = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coin['id']}/market_chart?vs_currency=usd&days={days}&interval=daily"
    )
    if r.ok:
        _coingecko_price_data[symbol] = r.json()
        _coingecko_price_data[symbol]["modified"] = datetime.now()


_coingecko_trending_data = []
_coingecko_trending_data_modified = datetime(2009, 1, 9)


def get_coingecko_trending_data():
    if (datetime.now() - _coingecko_trending_data_modified) > timedelta(hours=2):
        try_bg(_update_coingecko_trending_data, _coingecko_trending_data_modified)

    return _coingecko_trending_data


def _update_coingecko_trending_data():
    global _coingecko_trending_data
    global _coingecko_trending_data_modified

    r = requests.get("https://api.coingecko.com/api/v3/search/trending")
    if r.ok:
        _coingecko_trending_data = r.json()["coins"]
        _coingecko_trending_data_modified = datetime.now()


def try_bg(target, modified, args=()):
    if modified != datetime(2009, 1, 9):
        multiprocessing.Process(target=target, args=args).start()
    else:
        target(*args)

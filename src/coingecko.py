import requests
import json
import multiprocessing
import os
import redis

config = json.loads(open("../config.json").read())
cache = redis.from_url(os.getenv("REDIS_URL"))


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


def get_coingecko_coin_data():
    return get_data("_coingecko_coin_data", _set_coingecko_coin_data)


def _set_coingecko_coin_data():
    r = requests.get("https://api.coingecko.com/api/v3/search")
    if r.ok:
        data = json.dumps(r.json()["coins"])
        cache.set("_coingecko_coin_data", data, ex=hours(6))


def get_coingecko_price_data_by_symbol(symbol):
    return get_data(
        f"_coingecko_price_data={symbol}",
        _set_coingecko_price_data_by_symbol,
        args=(symbol,),
    )


def _set_coingecko_price_data_by_symbol(symbol):
    coin = get_coingecko_coin_data_by_symbol(symbol)
    if coin == None:
        cache.set(f"_coingecko_price_data={symbol}", "[]", ex=hours(6))
        return

    days = 366 if symbol == "BTC" else 32  # btc needs year of price data for chart
    r = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coin['id']}/market_chart?vs_currency=usd&days={days}&interval=daily"
    )
    if not r.ok:
        print(r.text, flush=True)
        cache.set(f"_coingecko_price_data={symbol}", "[]", ex=hours(1))
        return

    data = list(
        map(lambda p: [p[0], round(p[1], 2 if p[1] > 1 else 6)], r.json()["prices"])
    )
    cache.set(f"_coingecko_price_data={symbol}", json.dumps(data), ex=hours(2))


def get_coingecko_market_cap_data():
    return get_data("_coingecko_market_cap_data", _set_coingecko_market_cap_data)


def _set_coingecko_market_cap_data():
    r = requests.get(
        "https://www.coingecko.com/market_cap/total_charts_data?vs_currency=usd",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        },
    )
    if r.ok:
        data = json.dumps(r.json()["stats"])
        cache.set("_coingecko_market_cap_data", data, ex=hours(2))


def get_coingecko_trending_data():
    return get_data("_coingecko_trending_data", _set_coingecko_trending_data)


def _set_coingecko_trending_data():
    r = requests.get("https://api.coingecko.com/api/v3/search/trending")
    if r.ok:
        data = json.dumps(r.json()["coins"])
        cache.set("_coingecko_trending_data", data, ex=hours(2))


def get_data(key, update_function, args=()):
    if not cache.exists(key):
        update_function(*args)

    if cache.ttl(key) < hours(1):
        multiprocessing.Process(target=update_function, args=args).start()

    return json.loads(cache.get(key))


def hours(n):
    return n * 60 * 60


def cache_warm_up():
    multiprocessing.Process(target=_cache_warm_up).start()


def _cache_warm_up():
    _set_coingecko_coin_data()
    _set_coingecko_market_cap_data()
    _set_coingecko_trending_data()

    _set_coingecko_price_data_by_symbol("BTC")
    for coin in get_coingecko_trending_data():
        _set_coingecko_price_data_by_symbol(coin["item"]["symbol"])

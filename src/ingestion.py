import time
import logging
import json
import re
import praw
import textblob
import sqlite3
import multiprocessing

import database
import coingecko

config = json.loads(open("../config.json").read())
secrets = json.loads(open("../secrets.json").read())
symbol_regex = re.compile(r"\b[A-Z]{1,6}\b")
con = sqlite3.connect("../chatter.db")


def ingest(content_type, get_text):
    try:
        reddit = get_praw_instance(content_type)

        stream = reddit.stream.submissions
        if content_type == "comment":
            stream = reddit.stream.comments

        for item in stream(skip_existing=True):
            text = get_text(item)
            symbols = list(
                filter(
                    lambda symbol: coingecko.is_on_coingecko(symbol),
                    symbol_regex.findall(text),
                )
            )

            if len(symbols) == 0:
                continue

            polarity, subjectivity = analyze_text(text)

            for symbol in symbols:
                insert_symbol(symbol, content_type, polarity, subjectivity)

    except Exception as e:
        logging.exception(e)
        time.sleep(60)
        ingest(content_type, get_text)


def get_praw_instance(content_type):
    return praw.Reddit(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        user_agent=f"chatter_{content_type}s",
    ).subreddit("+".join(config["subreddits"]))


def analyze_text(text):
    tb = textblob.TextBlob(text)
    polarity = round(tb.sentiment.polarity, 1)
    subjectivity = round(tb.sentiment.subjectivity, 1)
    return (polarity, subjectivity)


def insert_symbol(symbol, content_type, polarity, subjectivity):
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO mentions (symbol, timestamp, content_type, polarity, subjectivity)
        VALUES (?, DATETIME('now'), ?, ?, ?);
        """,
        (symbol, content_type, polarity, subjectivity),
    )
    con.commit()


def ingest_in_background():
    database.init()

    ingest_args = [
        ("comment", lambda c: c.body),
        ("submission", lambda s: s.title + "\n" + s.selftext),
    ]

    for args in ingest_args:
        multiprocessing.Process(target=ingest, args=args).start()
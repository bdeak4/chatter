import multiprocessing
import time
import sqlite3
import json

from praw import Reddit
from reticker import TickerExtractor
from textblob import TextBlob

config = json.loads(open("config.json").read())
multireddit = "+".join(sum([config["subs"][k] for k in config["subs"]], []))
con = sqlite3.connect("data.db")


def fetch_reddit_submissions():
    reddit = Reddit(
        client_id=config["secrets"]["client_id"],
        client_secret=config["secrets"]["client_secret"],
        user_agent=config["secrets"]["user_agent"] + "__submissions",
    )
    reddit_subs = reddit.subreddit(multireddit)
    cur = con.cursor()
    te = TickerExtractor()
    try:
        for submission in reddit_subs.stream.submissions(skip_existing=True):
            text = submission.title + "\n" + submission.selftext
            polarity, subjectivity = text_sentiment(text)
            sub = submission.subreddit
            for ticker in te.extract(text):
                save_ticker(cur, ticker, sub, polarity, subjectivity, "post")
    except:
        time.sleep(60)
        fetch_reddit_submissions()


def fetch_reddit_comments():
    reddit = Reddit(
        client_id=config["secrets"]["client_id"],
        client_secret=config["secrets"]["client_secret"],
        user_agent=config["secrets"]["user_agent"] + "__comments",
    )
    reddit_subs = reddit.subreddit(multireddit)
    cur = con.cursor()
    te = TickerExtractor()
    try:
        for comment in reddit_subs.stream.comments(skip_existing=True):
            text = comment.body
            polarity, subjectivity = text_sentiment(text)
            sub = comment.subreddit
            for ticker in te.extract(text):
                save_ticker(cur, ticker, sub, polarity, subjectivity, "comment")
    except:
        time.sleep(60)
        fetch_reddit_comments()


def save_ticker(cur, ticker, sub, polarity, subjectivity, source):
    date = time.strftime("%Y-%m-%d")
    type_ = sub_type(sub)
    cur.execute(
        """
        INSERT INTO tickers (
            ticker, type, date, polarity, subjectivity, source, count
        ) VALUES (?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(
            ticker, type, date, polarity, subjectivity, source
        ) DO UPDATE SET count=count+1;
        """,
        (ticker, type_, date, polarity, subjectivity, source),
    )
    con.commit()


def sub_type(sub):
    for t in config["subs"]:
        if sub in config["subs"][t]:
            return t
    return ""


def text_sentiment(text):
    tb = TextBlob(text)
    pol = tb.sentiment.polarity
    subj = round(tb.sentiment.subjectivity)
    if pol > 0:
        return 1, subj
    if pol < 0:
        return -1, subj
    return 0, subj


def fetch_data_in_background():
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tickers (
            ticker TEXT,
            type TEXT,
            date TEXT,
            polarity INTEGER,
            subjectivity INTEGER,
            source TEXT,
            count INTEGER,
            UNIQUE(ticker, type, date, polarity, subjectivity, source)
        );
        """
    )
    con.commit()

    multiprocessing.Process(target=fetch_reddit_submissions).start()
    multiprocessing.Process(target=fetch_reddit_comments).start()

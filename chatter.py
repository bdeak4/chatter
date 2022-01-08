#!venv/bin/python

from bottle import route, run, template
import sqlite3
import json
import multiprocessing
import logging
import time
import re
import praw
import textblob
import reticker

config = json.loads(open("chatter.json").read())

con = sqlite3.connect("chatter.db")


# schema
# ------------------------------------------------------------------------------


con.execute(
    """
    CREATE TABLE IF NOT EXISTS asset_classes(
        asset_class TEXT UNIQUE
    );
    """
)
con.execute(
    """
    INSERT OR REPLACE INTO asset_classes(rowid, asset_class)
    VALUES
        (1, 'stocks'),
        (2, 'cryptocurrencies');
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS symbols(
        symbol TEXT UNIQUE,
        asset_class_id INTEGER,
        FOREIGN KEY(asset_class_id) REFERENCES asset_classes(rowid)
    );
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS dates(
        date TEXT UNIQUE
    );
    """
)
con.execute(
    """
    CREATE TABLE IF NOT EXISTS counts(
        date_id INTEGER,
        symbol_id INTEGER,
        polarity_negative_count INTEGER,
        polarity_neutral_count INTEGER,
        polarity_positive_count INTEGER,
        subjectivity_subjective_count INTEGER,
        subjectivity_objective_count INTEGER,
        source_post_count INTEGER,
        source_comment_count INTEGER,
        FOREIGN KEY(date_id) REFERENCES dates(rowid),
        FOREIGN KEY(symbol_id) REFERENCES symbols(rowid)
    );
    """
)
con.commit()


# ingestion
# ------------------------------------------------------------------------------


symbol_regex = re.compile(r"\b[A-Z]{1,6}\b")
multireddit = "+".join(sum(list(config["subreddits"].values()), []))


def ingest_submissions():
    try:
        reddit = praw.Reddit(
            client_id=config["secrets"]["client_id"],
            client_secret=config["secrets"]["client_secret"],
            user_agent="chatter_submissions",
        ).subreddit(multireddit)

        for submission in reddit.stream.submissions(skip_existing=True):
            text = submission.title + "\n" + submission.selftext
            ingest(text, "submission", asset_class(submission.subreddit))

    except Exception as e:
        logging.exception(e)
        time.sleep(60)
        ingest_submissions()


def ingest_comments():
    try:
        reddit = praw.Reddit(
            client_id=config["secrets"]["client_id"],
            client_secret=config["secrets"]["client_secret"],
            user_agent="chatter_comments",
        ).subreddit(multireddit)

        for comment in reddit.stream.comments(skip_existing=True):
            ingest(comment.body, "comment", asset_class(comment.subreddit))

    except Exception as e:
        logging.exception(e)
        time.sleep(60)
        ingest_comments()


def ingest(text, source, asset_class):
    tb = textblob.TextBlob(text)
    symbols = symbol_regex.findall(text)
    print(text)
    print(symbols)
    print(asset_class)
    print(round(tb.sentiment.polarity), round(tb.sentiment.subjectivity))


def asset_class(subreddit):
    for ac, subreddits in config["subreddits"].items():
        if str(subreddit).lower() in subreddits:
            return ac


ingest_comments()


# routes
# ------------------------------------------------------------------------------


@route("/")
def index():
    cur = con.cursor()
    return "hi2"


run(host="0.0.0.0", port=8080, server="waitress")

con.close()

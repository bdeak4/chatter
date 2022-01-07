#!venv/bin/python

from bottle import route, run, template
import sqlite3

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


print("hi")


# routes
# ------------------------------------------------------------------------------


@route("/")
def index():
    cur = con.cursor()
    return "hi2"


run(host="0.0.0.0", port=8080, server="waitress")

con.close()

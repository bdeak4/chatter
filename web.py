#!venv/bin/python

from bottle import route, run, template, static_file
import sqlite3

from ingestion import ingest_in_background


con = sqlite3.connect("chatter.db")
cur = con.cursor()


@route("/")
def index():
    return template("index.html")


@route("/static/<filepath:path>")
def static(filepath):
    return static_file(filepath, root="static")


ingest_in_background()

run(host="0.0.0.0", port=8080, server="waitress")

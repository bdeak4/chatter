bind = "0.0.0.0:5000"
workers = 4

import database
import ingestion
import coingecko


def on_starting(server):
    database.migrate()
    ingestion.ingest_in_background()
    coingecko.cache_warm_up()
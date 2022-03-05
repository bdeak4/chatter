from datetime import date, timedelta


def sql_time_interval(time_period):
    if time_period == "week":
        return "-6 days"

    if time_period == "month":
        return "-1 month"

    if time_period == "quarter":
        return "-3 months"

    if time_period == "year":
        return "-1 year"


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n + 1)


def date_months_ago(n):
    today = date.today()
    month = today.month - n
    year = today.year
    while month < 1:
        month += 12
        year -= 1
    return date(year, month, today.day)


def start_date(time_period):
    if time_period == "week":
        return date.today() - timedelta(days=7)

    if time_period == "month":
        return date_months_ago(1)

    if time_period == "quarter":
        return date_months_ago(3)

    if time_period == "year":
        return date_months_ago(12)


def fill_blanks(time_period, rows):
    blank_cols = len(rows[0]) - 1
    all_rows = []

    for d in daterange(start_date(time_period), date.today()):
        ts = d.strftime("%Y-%m-%d")
        existing_row = next(filter(lambda row: row[0] == ts, rows), None)
        if existing_row != None:
            all_rows.append(existing_row)
            continue

        blank_row = (ts,) + tuple(0 for _ in range(0, blank_cols))
        all_rows.append(blank_row)

    return all_rows

from datetime import date, timedelta


def sql_time_interval(time_period):
    if time_period == "week":
        return "1 WEEK"

    if time_period == "month":
        return "1 MONTH"

    if time_period == "quarter":
        return "3 MONTH"

    if time_period == "year":
        return "1 YEAR"


def sql_time_period_from_ts(time_period):
    if time_period == "day":
        return "timestamp::DATE"

    if time_period == "week":
        return "EXTRACT(DOW FROM timestamp)"

    if time_period == "month":
        return "EXTRACT(MONTH FROM timestamp)"


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n + 1)


def time_period_len(time_period):
    return len(list(daterange(start_date(time_period), date.today())))


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
    if not len(rows):
        return []

    blank_cols = len(rows[0]) - 1
    all_rows = []

    for d in daterange(start_date(time_period), date.today()):
        existing_row = next(filter(lambda row: row[0] == d, rows), None)
        if existing_row != None:
            all_rows.append(existing_row)
            continue

        blank_row = (d,) + tuple(0 for _ in range(0, blank_cols))
        all_rows.append(blank_row)

    return all_rows

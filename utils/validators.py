from datetime import datetime


def valid_date(
    value
):

    try:

        datetime.strptime(
            value,
            "%Y-%m-%d"
        )

        return True

    except ValueError:

        return False
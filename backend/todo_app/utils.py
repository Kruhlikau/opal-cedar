import datetime


def get_time_of_day():
    now = datetime.datetime.now()
    if 5 <= now.hour < 12:
        return "morning"
    elif 12 <= now.hour < 18:
        return "afternoon"
    else:
        return "evening"


def is_working_day():
    """Check if today is a working day (Monday to Friday)."""
    today = datetime.date.today().weekday()
    return today < 5

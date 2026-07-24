import json
from pathlib import Path
from datetime import datetime, timedelta

from economic_calendar import get_calendar


CALENDAR_FILE = Path("/root/TradeMindAI/calendar.json")


def update_calendar():

    events = get_calendar()

    if events:

        data = {
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "events": events
        }

        with open(
            CALENDAR_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    return events



def get_calendar_cached():

    if not CALENDAR_FILE.exists():

        return update_calendar()


    with open(
        CALENDAR_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    updated = datetime.strptime(
        data["updated"],
        "%Y-%m-%d %H:%M:%S"
    )


    if datetime.now() - updated > timedelta(hours=1):

        return update_calendar()


    return data["events"]
import json
from pathlib import Path
from datetime import datetime, timedelta

from economic_calendar import get_calendar


CACHE_FILE = Path("/root/TradeMindAI/news.json")


def update_news():

    events = get_calendar()

    data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "events": events
    }

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    return events



def get_cached_news():

    if not CACHE_FILE.exists():
        return update_news()


    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)


    updated = datetime.strptime(
        data["updated"],
        "%Y-%m-%d %H:%M:%S"
    )


    # обновляем раз в час
    if datetime.now() - updated > timedelta(hours=1):
        return update_news()


    return data["events"]

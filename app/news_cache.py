from pathlib import Path
import json
from datetime import datetime, timedelta

from economic_calendar import get_calendar


NEWS_FILE = Path("/root/TradeMindAI/news.json")


def update_news():

    events = get_calendar()

    if events:
        data = {
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "events": events
        }

        with open(
            NEWS_FILE,
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


def get_cached_news():

    if not NEWS_FILE.exists():
        return update_news()

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    updated = datetime.strptime(
        data["updated"],
        "%Y-%m-%d %H:%M"
    )

    if datetime.now() - updated > timedelta(hours=1):
        return update_news()

    return data["events"]


def get_cache():

    if not NEWS_FILE.exists():
        update_news()

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)
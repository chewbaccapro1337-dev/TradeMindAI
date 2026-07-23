import json
from pathlib import Path
from datetime import datetime
from economic_calendar import get_calendar


NEWS_FILE = Path("/root/TradeMindAI/news.json")


def update_news():

    events = get_calendar()

    if not events:
        return False

    data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "events": events
    }

    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

    return True



def get_news(currency=None, only_high=False):

    if not NEWS_FILE.exists():
        update_news()

    with open(
        NEWS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
       data = json.load(f)
       events = data.get("events", [])


    if currency:
        events = [
            e for e in events
            if e["currency"] == currency
        ]


    if only_high:
        events = [
            e for e in events
            if e["impact"] == "red"
        ]


    return events

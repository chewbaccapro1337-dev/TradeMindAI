from pathlib import Path
import json
from datetime import datetime

from economic_calendar import get_calendar


CACHE = Path("/root/TradeMindAI/news.json")


def update_news():

    if CACHE.exists():

        with open(CACHE, "r", encoding="utf-8") as f:
            old = json.load(f)

        updated = datetime.fromisoformat(
            old["updated"]
        )

        diff = datetime.now() - updated

        if diff.total_seconds() < 3600:
            return old["events"]


    events = get_calendar()


    data = {
        "updated": datetime.now().isoformat(),
        "events": events
    }


    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


    return events

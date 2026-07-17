import json
from pathlib import Path


NEWS_FILE = Path("/root/TradeMindAI/news.json")


def get_news(only_high=False):

    if not NEWS_FILE.exists():
        return []

    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        events = json.load(f)

    if only_high:
        events = [
            e for e in events
            if e["impact"] == "red"
        ]

    return events

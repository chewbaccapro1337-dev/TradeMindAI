import json
import requests
from pathlib import Path
from datetime import datetime, timedelta


NEWS_FILE = Path("/root/TradeMindAI/news.json")


def need_update():

    if not NEWS_FILE.exists():
        return True

    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = datetime.strptime(
        data["updated"],
        "%Y-%m-%d %H:%M:%S"
    )

    return datetime.now() - updated > timedelta(hours=1)



def update_news():

    if not need_update():
        return


    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }


    # тут будет источник
    response = requests.get(
        "ССЫЛКА_НА_ИСТОЧНИК",
        headers=headers,
        timeout=15
    )


    events = []


    data = {
        "updated":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
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
from pathlib import Path
import json
from datetime import datetime, timedelta


CACHE_FILE = Path("/root/TradeMindAI/ai_calendar.json")


def get_ai_cache():

    if not CACHE_FILE.exists():
        return None


    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)


    updated = datetime.strptime(
        data["updated"],
        "%Y-%m-%d %H:%M:%S"
    )


    if datetime.now() - updated > timedelta(hours=3):
        return None


    return data["analysis"]



def save_ai_cache(analysis):

    data = {
        "updated": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "analysis": analysis
    }


    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

import json
from pathlib import Path


CACHE_FILE = Path("news_ai_cache.json")


def load_cache():

    if not CACHE_FILE.exists():
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_cache(data):

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



def get_cached_analysis(key):

    cache = load_cache()

    return cache.get(key)



def save_analysis(key, result):

    cache = load_cache()

    cache[key] = result

    save_cache(cache)

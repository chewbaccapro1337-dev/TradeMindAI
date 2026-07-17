import requests

API_KEY = "d9d5809r01qj7sqb2e2gd9d5809r01qj7sqb2e30"

def get_calendar():
    url = (
        f"https://finnhub.io/api/v1/calendar/economic"
        f"?from=2026-07-17&to=2026-07-24&token={API_KEY}"
    )

    r = requests.get(url)

    if r.status_code != 200:
        return {"error": r.text}

    return r.json()

import requests

RAPID_KEY = "e849991ff5msh405c6b4dc517478p1ac0a7jsna4ba8db9ba05"

url = "https://multilingual-economic-calendar-api-by-truedata.p.rapidapi.com/economic-events/filter"

headers = {
    "x-rapidapi-key": RAPID_KEY,
    "x-rapidapi-host": "multilingual-economic-calendar-api-by-truedata.p.rapidapi.com"
}


def get_calendar():

    params = {
        "date_from": "2026-07-17",
        "date_to": "2026-07-24",
        "currency": "USD",
        "importance": "high",
        "lang": "en"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )

    return response.json()

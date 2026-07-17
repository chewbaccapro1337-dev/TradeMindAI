import requests
from bs4 import BeautifulSoup


def get_calendar():

    url = "https://www.forexfactory.com/calendar"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers, timeout=20).text

    print(html[:500])

    return html

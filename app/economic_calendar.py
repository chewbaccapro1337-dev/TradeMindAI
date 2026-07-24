import feedparser
from datetime import datetime


FEEDS = [
    "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
]


def get_calendar():

    events = []

    feed = feedparser.parse(FEEDS[0])


    for item in feed.entries:

        title = item.get("title", "")
        description = item.get("description", "")


        text = title + " " + description


        currency = None

        if "USD" in text:
            currency = "USD"

        elif "EUR" in text:
            currency = "EUR"

        elif "GBP" in text:
            currency = "GBP"


        if not currency:
            continue


        impact = "yellow"


        if "High" in text or "HIGH" in text:
            impact = "red"


        time = item.get(
            "published",
            ""
        )


        events.append(
            {
                "currency": currency,
                "impact": impact,
                "title": title,
                "time": time
            }
        )


    return events
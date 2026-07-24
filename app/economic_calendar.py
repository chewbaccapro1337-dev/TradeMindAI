import feedparser
from datetime import datetime


FEEDS = [
    "https://www.fxstreet.com/rss/news",
]


def get_calendar():

    events = []


    for url in FEEDS:

        feed = feedparser.parse(url)


        for item in feed.entries[:30]:

            title = item.get(
                "title",
                ""
            )


            published = item.get(
                "published",
                ""
            )


            text = title.lower()


            currency = None


            if "usd" in text or "dollar" in text:
                currency = "USD"

            elif "eur" in text or "euro" in text:
                currency = "EUR"

            elif "gbp" in text or "pound" in text:
                currency = "GBP"



            if currency:

                events.append({

                    "currency": currency,

                    "impact": "red",

                    "title": title,

                    "time": published

                })


    return events

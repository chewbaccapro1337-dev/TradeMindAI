import feedparser
from datetime import datetime


FXSTREET_RSS = "https://www.fxstreet.com/rss/news"


def get_calendar():

    events = []

    try:
        feed = feedparser.parse(FXSTREET_RSS)

        for item in feed.entries[:30]:

            title = item.get("title", "")
            summary = item.get("summary", "")

            text = (title + " " + summary).upper()

            currency = None

            if "USD" in text or "FED" in text or "FOMC" in text:
                currency = "USD"

            elif "EUR" in text or "ECB" in text:
                currency = "EUR"

            elif "GBP" in text or "BOE" in text:
                currency = "GBP"


            if currency:

                events.append(
                    {
                        "currency": currency,
                        "impact": "red",
                        "title": title,
                        "time": datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    }
                )


    except Exception as e:
        print("FXStreet error:", e)


    return events
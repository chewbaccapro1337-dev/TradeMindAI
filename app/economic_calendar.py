import requests
from bs4 import BeautifulSoup


URL = "https://www.myfxbook.com/forex-economic-calendar"


def get_calendar():

    events = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    try:

        r = requests.get(
            URL,
            headers=headers,
            timeout=10
        )


        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )


        rows = soup.find_all(
            "tr"
        )


        for row in rows:

            cols = row.find_all("td")


            if len(cols) < 5:
                continue


            currency = cols[1].text.strip()
            impact = cols[2].text.strip()
            title = cols[3].text.strip()
            time = cols[0].text.strip()


            if currency in [
                "USD",
                "EUR",
                "GBP"
            ]:

                events.append(
                    {
                        "currency": currency,
                        "impact": "red" if "High" in impact else "yellow",
                        "title": title,
                        "time": time
                    }
                )


    except Exception as e:

        print("Calendar error:", e)


    return events
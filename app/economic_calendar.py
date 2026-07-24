from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


URL = "https://www.forexfactory.com/calendar"


def get_calendar():

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"
    )


    driver = webdriver.Chrome(
        options=options
    )


    events = []


    try:

        driver.get(URL)

        time.sleep(5)


        html = driver.page_source


        with open(
            "/root/TradeMindAI/ff_debug.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(html)



        soup = BeautifulSoup(
            html,
            "lxml"
        )


        rows = soup.select(
            "tr.calendar__row"
        )


        print(
            "ROWS:",
            len(rows)
        )


        for row in rows:


            currency = row.select_one(
                ".calendar__currency"
            )

            title = row.select_one(
                ".calendar__event-title"
            )

            impact = row.select_one(
                ".calendar__impact"
            )

            event_time = row.select_one(
                ".calendar__time"
            )


            if not currency or not title:
                continue


            cur = currency.text.strip()


            if cur not in [
                "USD",
                "EUR",
                "GBP"
            ]:
                continue



            level = "yellow"


            if impact:

               impact_html = str(impact)

               if "icon--ff-impact-red" in impact_html:
                   level = "red"

               elif "icon--ff-impact-ora" in impact_html:
                   level = "orange"

               elif "icon--ff-impact-yel" in impact_html:
                   level = "yellow"



            events.append({

                "currency": cur,

                "impact": level,

                "title": title.text.strip(),

                "time":
                    event_time.text.strip()
                    if event_time
                    else ""

            })


        return events


    finally:

        driver.quit()

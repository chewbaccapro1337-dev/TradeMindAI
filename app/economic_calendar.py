import requests
from jb_news.news import JBNews

API_KEY = "PCMdc1YONIzbla9skEdRl9Z5HRJIbjho"

jb = JBNews()


def get_calendar():

    if jb.calendar(
        API_KEY,
        today=True
    ):

        return jb.calendar_info

    return []

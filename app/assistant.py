from analysis import make_report
from statistics import show_statistics
from ai import ask_ai


def process_message(text: str):

    text = text.lower()

    if "btc" in text or "битк" in text:
        return make_report()

    if "стат" in text:
        return "Статистика пока в разработке."

    if "новост" in text:
        return "Новости пока в разработке."

    return ask_ai(text)
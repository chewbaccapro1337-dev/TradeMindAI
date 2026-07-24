import os
from openai import OpenAI
from dotenv import load_dotenv
from ai_calendar_cache import (
    get_ai_cache,
    save_ai_cache
)

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def analyze_calendar(events):

    cached = get_ai_cache()

    if cached:
        return cached

    if not events:
        return "📭 Экономических событий нет."


    calendar_text = ""

    for e in events[:20]:

        impact = e.get("impact", "")

        calendar_text += (
            f"{e.get('currency')} | "
            f"{e.get('time')} | "
            f"{e.get('title')} | "
            f"Impact: {impact}\n"
        )


    prompt = f"""
Ты профессиональный трейдер ICT / Smart Money Concepts.

Проанализируй экономический календарь на сегодня.

Цель:
дать трейдеру понимание рисков перед торговлей BTC, XAUUSD, EURUSD, GBPUSD.

Календарь:

{calendar_text}


Ответ строго в формате:

🧠 TRADEMIND AI
══════════════════

📅 Экономический обзор дня

Напиши главные события и их влияние.


🔥 HIGH IMPACT СОБЫТИЯ

Выдели самые опасные события.


💵 Влияние на USD

Как новости могут повлиять на доллар.


₿ Влияние на BTC

Риск для крипторынка.


📈 Торговый план

Когда лучше ждать вход.
Когда избегать торговли.


⚠️ Риск дня

Низкий / Средний / Высокий

Краткое объяснение.
"""


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )


    analysis = response.output_text

    save_ai_cache(analysis)

    return analysis

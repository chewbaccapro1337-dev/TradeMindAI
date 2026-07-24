import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from news_ai_cache import (
    get_cached_analysis,
    save_analysis
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def analyze_trade(image_path: str):

    with open(image_path, "rb") as image:
        image_base64 = base64.b64encode(image.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": ( f"""
                         Ты — профессиональный трейдер ICT / Smart Money Concepts.

                         Проанализируй изображение графика.

                         Ответ верни ТОЛЬКО в таком формате.

                         🧠 TRADEMIND AI
                         ══════════════════════

                         📊 АНАЛИЗ СДЕЛКИ

                         📈 Инструмент
                         Определи инструмент, если его видно. Если нет — напиши "Не определён".

                         ══════════════════════

                         🎯 Направление

                         Укажи:
                         🟢 BUY
                         или
                         🔴 SELL

                         Комментарий:
                         Кратко объясни идею входа.

                         ══════════════════════

                         ⭐ Качество входа

                         Поставь оценку от ★☆☆☆☆ до ★★★★★.

                         После оценки напиши:

                         • качество входа
                         • качество стопа
                         • качество подтверждения
                               
                         ══════════════════════

                         💧 Smart Money

                         Для каждого пункта напиши либо ✅ либо ❌

                         ✅ Liquidity Grab

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ Order Block 

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ Fair Value Gap

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ CHoCH

                         краткое пояснение

                         ━━━━━━━━━━━━━━━━━━

                         ✅ BOS

                         краткое пояснение

                         ══════════════════════

                         ⚖️ Risk / Reward

                         Если видно RR —
                         укажи его.

                         Если нет —
                         напиши "Не удалось определить".

                         После этого дай оценку RR.

                         ══════════════════════

                         ⚠️ Что можно улучшить

                         Напиши 3-5 рекомендаций списком.

                         ══════════════════════

                         🏆 Итоговая оценка

                         Оцени сделку от 0 до 100.

                         Потом поставь рейтинг

                         ⭐⭐☆☆☆
                         или
                         ⭐⭐⭐⭐⭐

                         Вердикт:

                         2-3 предложения с общим выводом.

                         Заканчивай сообщение строкой

                         🤖 TradeMind AI

                         Никаких дополнительных объяснений вне этого шаблона не добавляй.
                         """
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    return response.output_text


def analyze_economic_event(event):

    key = (
        f"{event['currency']}_"
        f"{event['title']}_"
        f"{event.get('actual')}"
    )


    cached = get_cached_analysis(key)

    if cached:
        return cached


    prompt = f"""
Ты профессиональный трейдер.



Проанализируй экономическую новость:

Валюта:
{event['currency']}

Событие:
{event['title']}

Прогноз:
{event.get('forecast')}

Факт:
{event.get('actual')}


Ответ строго:

🔥 Сила новости:
от 1 до 5


💵 USD:
🟢 рост
или
🔴 падение


₿ BTC:
🟢 рост
или
🔴 падение


📊 Анализ:
2-3 предложения.


🎯 Торговый сценарий:
что ждать после выхода новости.
"""


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.3
    )


    result = response.choices[0].message.content


    save_analysis(
        key,
        result
    )


    return result

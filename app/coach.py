from openai import OpenAI
import os

from database import get_connection


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_closed_trade(user_id, trade_id):

    print("COACH START:", user_id, trade_id)

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            symbol,
            side,
            entry,
            tp,
            sl,
            risk,
            pnl,
            comment,
            market_context,
            entry_reason
        FROM trades
        WHERE id = ?
        AND user_id = ?
    """,
    (
        trade_id,
        user_id
    ))


    trade = cursor.fetchone()


    conn.close()


    if not trade:
        return None


    symbol, side, entry, tp, sl, risk, pnl, comment, entry_reason, market_context = trade

    import json

    context = json.loads(market_context)

    market_summary = {
        "trend": context.get("trend"),
        "bos_choch": context.get("bos_choch"),
        "sweep": context.get("sweep"),
        "fvgs": context.get("fvgs"),
        "market_structure": context.get("market_structure")
    }

    prompt = f"""

Ты — AI Trading Coach.

Проанализируй закрытую сделку трейдера.


Сделка:

{market_summary}

Инструмент:
{symbol}

Направление:
{side}

Вход:
{entry}

TP:
{tp}

SL:
{sl}

Риск:
{risk}

Результат:
{pnl}

Контекст рынка в момент входа:

{market_context}

Оцени сделку от 1 до 10:

10 — идеальный ICT/SMC сетап
1 — случайный вход без подтверждений

Дай анализ:

1. Была ли ошибка?
2. Какая ошибка вероятнее всего?
3. Нарушена ли стратегия ICT/SMC?
4. Что сделать лучше в следующей сделке?

Причина входа трейдера:
{entry_reason}

Сравни:
- что хотел увидеть трейдер
- что реально было в market_context

Дай ответ строго в формате:

🤖 AI Coach

Оценка сделки: X/10

━━━━━━━━━━━━━━

❌ Ошибки:
- перечисли конкретные ошибки только по данным сделки и market_context

━━━━━━━━━━━━━━

✅ Хорошие моменты:
- что было сделано правильно

━━━━━━━━━━━━━━

🎯 Главная ошибка:
одно главное нарушение

━━━━━━━━━━━━━━

📚 Что делать в следующей сделке:
3 конкретных правила

━━━━━━━━━━━━━━

Не выдумывай события, которых нет в данных.
Если BOS/CHOCH/Sweep/FVG отсутствуют в анализе — напиши именно это.
"""


    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0.3,
        messages=[
            {
                "role":"system",
                "content":
                "Ты строгий торговый наставник."
            },
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    return response.choices[0].message.content



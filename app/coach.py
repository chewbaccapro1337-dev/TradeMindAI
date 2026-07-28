from openai import OpenAI
import os

from database import get_connection


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_closed_trade(user_id, trade_id):

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
            comment
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


    symbol, side, entry, tp, sl, risk, pnl, comment = trade


    prompt = f"""

Ты — AI Trading Coach.

Проанализируй закрытую сделку трейдера.


Сделка:

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

Комментарий трейдера:
{comment}


Дай анализ:

1. Была ли ошибка?
2. Какая ошибка вероятнее всего?
3. Нарушена ли стратегия ICT/SMC?
4. Что сделать лучше в следующей сделке?


Ответь коротко как личный торговый наставник.
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

def analyze_closed_trade(user_id, trade_id):

    print("COACH START", user_id, trade_id)

    return "Тест AI Coach работает"
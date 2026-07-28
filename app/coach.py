from openai import OpenAI
import os

from database import (
    get_connection,
    get_last_closed_trades
)


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

    recent_trades = get_last_closed_trades(
     user_id,
        limit=20
    )

    history_text = ""

    for t in recent_trades:
        trade_id, symbol_h, side_h, pnl_h, context_h = t

        history_text += f"""

    Сделка #{trade_id}
    Инструмент: {symbol_h}
    Направление: {side_h}
    Результат: {pnl_h}

    Контекст:
    {context_h}

    ----------------
    """

    import json

    if market_context:
        context = json.loads(market_context)
    else:
        context = {}

    market_summary = {
        "trend": context.get("trend"),
        "bos_choch": context.get("bos_choch"),
        "sweep": context.get("sweep"),
        "fvgs": context.get("fvgs"),
        "market_structure": context.get("market_structure")
    }

    prompt = f"""

Ты — AI Trading Coach.

Ты профессиональный наставник по ICT / Smart Money Concepts.

Твоя задача — не просто оценить одну сделку, а найти ошибки трейдера и повторяющиеся паттерны поведения.


━━━━━━━━━━━━━━
ТЕКУЩАЯ ЗАКРЫТАЯ СДЕЛКА
━━━━━━━━━━━━━━


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


Market context в момент входа:

{json.dumps(context, indent=2, ensure_ascii=False)}


Причина входа трейдера:

{entry_reason}


━━━━━━━━━━━━━━
История последних закрытых сделок:
━━━━━━━━━━━━━━


{history_text}


Проанализируй:


1. Оцени текущую сделку от 1 до 10.

10 — идеальный ICT/SMC сетап:
- есть ликвидность
- есть sweep
- есть BOS/CHOCH
- есть displacement
- есть FVG/OB зона
- вход соответствует контексту


1 — случайный вход:
- нет подтверждения
- вход против структуры
- эмоциональное решение


2. Определи:


А) Ошибка в текущей сделке:
- что сделал трейдер неправильно?
- какой конкретно элемент ICT/SMC отсутствовал?


Б) Сравни:


Что хотел увидеть трейдер:
{entry_reason}


Что реально было:
market_context


В) Найди повторяющиеся ошибки:


Проанализируй последние сделки.

Если есть повторяющийся паттерн:

пример:

"4 из последних 6 убыточных сделок были входы без BOS/CHOCH"

или

"Трейдер часто входит в RANGE без подтверждения"


Укажи это.


Г) Создай правило для трейдера:


Например:

"Следующие 5 сделок нельзя открывать без CHOCH"

или

"В RANGE торговать только от границ диапазона"


━━━━━━━━━━━━━━


Ответ строго в формате:


🤖 AI Coach


⭐ Оценка сделки: X/10


━━━━━━━━━━━━━━


❌ Ошибки текущей сделки:

- конкретные ошибки только на основе данных


━━━━━━━━━━━━━━


✅ Хорошие моменты:

- что было сделано правильно


━━━━━━━━━━━━━━


🎯 Главная ошибка:

одно главное нарушение


━━━━━━━━━━━━━━


📊 Повторяющиеся ошибки трейдера:

- найди паттерны из истории сделок
- если данных недостаточно — напиши это


━━━━━━━━━━━━━━


📚 Персональное правило:

одно правило, которое трейдер должен соблюдать следующие сделки


━━━━━━━━━━━━━━


Не выдумывай данные.

Если BOS/CHOCH/Sweep/FVG отсутствуют — укажи, что их нет.

Если история сделок недостаточная — скажи об этом.

Не обвиняй трейдера.
Действуй как строгий профессиональный торговый наставник.

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



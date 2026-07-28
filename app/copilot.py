from database import get_connection


def get_trading_history(user_id, limit=50):

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
            created_at
        FROM trades
        WHERE user_id = ?
        AND status = 'CLOSED'
        ORDER BY created_at DESC
        LIMIT ?

    """, (user_id, limit))


    trades = cursor.fetchall()

    conn.close()

    return trades


def trade_copilot_tool(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            symbol,
            side,
            entry,
            tp,
            sl,
            pnl,
            status
        FROM trades
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,))


    trades = cursor.fetchall()

    conn.close()


    if not trades:
        return """
У пользователя пока нет сделок.

Нельзя анализировать торговое поведение.
"""


    text = "Последние сделки пользователя:\n\n"


    for t in trades:

        text += f"""
Инструмент: {t[0]}
Направление: {t[1]}
Вход: {t[2]}
TP: {t[3]}
SL: {t[4]}
PNL: {t[5]}
Статус: {t[6]}

"""


    return text

def build_copilot_data(user_id):

    trades = get_trading_history(user_id)


    if not trades:
        return "Нет закрытых сделок для анализа."


    text = """
История сделок трейдера:

"""


    for t in trades:

        (
            symbol,
            side,
            entry,
            tp,
            sl,
            risk,
            pnl,
            comment,
            date
        ) = t


        text += f"""
Дата: {date}

Инструмент:
{symbol}

Направление:
{side}

Entry:
{entry}

TP:
{tp}

SL:
{sl}

Риск:
{risk}

Результат:
{pnl}

Комментарий:
{comment}

-----------------

"""


    return text
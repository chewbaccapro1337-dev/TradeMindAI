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
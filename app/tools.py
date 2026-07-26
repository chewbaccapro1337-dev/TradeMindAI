def btc_analysis_tool(user_id, text=None):

    from analysis import make_report

    return make_report()



def statistics_tool(user_id):

    from journal import build_statistics_text

    return build_statistics_text(
        user_id
    )



def last_trades_tool(user_id):

    from journal import build_last_trades_text

    return build_last_trades_text(
        user_id
    )

def news_tool(user_id, symbol=None):

    from news import build_news_text

    print("NEWS SYMBOL:", symbol)

    return build_news_text(symbol)

def market_brief_tool(user_id, *_):

    from analysis import make_report
    from news import build_news_text
    from openai import OpenAI
    import os

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    btc = make_report()
    news = build_news_text()

    prompt = f"""
Ты главный аналитик TradeMind AI.

Проанализируй данные ниже.

Не копируй их.

Сделай полноценный обзор рынка.

Структура ответа:

📊 Общая картина рынка

🌍 Фундамент

₿ Bitcoin

🎯 Что лучше делать сегодня интрадей трейдеру

⚠️ Основные риски

📌 Итог

Новости:

{news}

BTC:

{btc}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "Ты профессиональный аналитик крипто и форекс рынка."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def create_trade_tool(user_id, text):

    from trade_voice import parse_trade_voice

    return parse_trade_voice(
        user_id,
        text
    )


def close_trade_tool(user_id, text):

    import re

    from database import close_last_trade

    text_lower = text.lower()

    symbol = None

    if "eur" in text_lower or "евро" in text_lower:
        symbol = "EURUSD"

    elif "gbp" in text_lower:
        symbol = "GBPUSD"

    elif "btc" in text_lower:
        symbol = "BTCUSDT"

    elif "eth" in text_lower:
        symbol = "ETHUSDT"


    price = re.search(
        r"(\d+(?:\.\d+)?)",
        text
    )

    if not price:
        return "❌ Не понял цену закрытия."

    exit_price = float(
        price.group(1)
    )

    result = close_last_trade(
        user_id,
        exit_price,
        symbol
    )

    if not result:
        return "📭 Нет открытых сделок."

    return (
        f"✅ Сделка закрыта\n\n"
        f"📌 {result['symbol']}\n"
        f"📈 {result['side']}\n"
        f"📥 Вход: {result['entry']}\n"
        f"📤 Выход: {result['exit']}\n"
        f"💰 PNL: {result['pnl']:.2f}"
    )

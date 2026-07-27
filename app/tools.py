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

def market_brief_tool(user_id, symbol=None, market=None):

    from analysis import make_report
    from news import build_news_text
    from market_context import get_market_context
    from openai import OpenAI
    import os

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    if symbol is None:
     symbol = "BTCUSDT"

    if market is None:
        market = "crypto"
    else:
        market_type = market

    analysis = make_report(symbol)

    market = get_market_context()

    news = build_news_text()

    if market_type == "forex":

     intro = """
Ты анализируешь рынок Forex.

Главное внимание уделяй:

- экономическому календарю
- DXY
- золоту
- валютной паре
"""

    else:

     intro = """
Ты анализируешь крипторынок.

Главное внимание уделяй:

- BTC
- DXY
- SP500
- золоту
- настроению риска
"""

    prompt = f"""
    {intro}

Ты главный аналитик TradeMind AI.

Ты работаешь как профессиональный трейдер и макро-аналитик.

Твоя задача — объединить технический анализ, межрыночные данные и фундаментальные события в единый торговый вывод.

Учитывай:

Технический анализ инструмента {symbol}:

{analysis}


🌍 Межрыночный анализ:

{market_data}

Включает:
- DXY (индекс доллара)
- золото
- S&P500


📰 Экономический календарь:

{news}


Правила анализа:

- Не копируй исходные данные.
- Не перечисляй просто показатели.
- Объясни взаимосвязи между рынками.
- Определи режим рынка: Risk ON или Risk OFF.
- Укажи, поддерживает ли макро фон рост или падение BTC.
- Дай практический вывод для интрадей трейдера.


Структура ответа:

📊 Общая картина рынка

Определи текущее состояние рынка.


🌍 Макро фон

DXY:
Gold:
S&P500:
Что это значит для риск-активов.


📰 Фундамент

Главные события из календаря и их возможное влияние.


₿ Bitcoin

Техническая картина:
- тренд
- структура
- ликвидность
- возможные сценарии


🎯 Торговый план на сегодня

Что лучше делать трейдеру:
- искать покупки
- искать продажи
- ждать подтверждение


⚠️ Основные риски

Какие события могут изменить сценарий.


📌 Итог

Краткий вывод одним абзацем.

Новости:

{news}

Технический анализ {symbol}:

{analysis}


Межрыночный анализ:

{market_data}
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

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


    analysis = make_report(symbol)

    market_data = get_market_context()

    news = build_news_text()



    if market == "forex":

        intro = """
Ты анализируешь Forex.

Главное:
- DXY
- экономический календарь
- центральные банки
- валютная пара
"""

    else:

        intro = """
Ты анализируешь крипторынок.

Главное:
- BTC/ETH
- DXY
- SP500
- Risk ON/OFF
"""



    prompt = f"""

{intro}


Ты — TradeMind AI.
Ты не пишешь статью.
Ты даёшь короткий профессиональный торговый бриф для интрадей трейдера.


Инструмент:

{symbol}



Технический анализ:

{analysis}



Макро данные:

{market_data}



Новости:

{news}



Твои задачи:


1. Определи режим рынка:

Risk ON / Risk OFF / NEUTRAL


2. Определи торговое направление:

BUY
SELL
WAIT


3. Оцени качество сетапа:

от 1 до 10


4. Найди главное:

- есть ли BOS/CHOCH
- есть ли Sweep
- есть ли FVG
- есть ли хорошая зона входа


5. Дай конкретный план.


Не выдумывай данные.
Если элемента нет — пиши "нет".



Формат ответа строго:


🤖 TradeMind AI

📌 {symbol}

━━━━━━━━━━━━━━

🌍 Режим рынка:
(Risk ON/OFF)


📈 Направление:
BUY / SELL / WAIT


⭐ Качество:
X/10


━━━━━━━━━━━━━━

🧠 Структура:

Тренд:
...

BOS/CHOCH:
...

Sweep:
...

FVG:
...


━━━━━━━━━━━━━━

🎯 Торговый план:

Вход:
...

Подтверждение:
...

Отмена сценария:
...


━━━━━━━━━━━━━━

⚠️ Риски:

- 3 главных риска


━━━━━━━━━━━━━━

Итог:
2-3 предложения максимум.


Ответ максимум 1200 символов.
"""


    response = client.chat.completions.create(

        model="gpt-5.4-mini",

        temperature=0.2,

        messages=[
            {
                "role": "system",
                "content": "Ты профессиональный ICT/SMC трейдер и макроаналитик."
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

def trade_copilot_tool(user_id):

    from copilot import build_copilot_data
    from openai import OpenAI
    import os


    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


    trades = build_copilot_data(user_id)


    prompt = f"""

Ты являешься AI Trading Copilot.

Проанализируй историю сделок трейдера.

Найди:

- главные ошибки
- повторяющиеся паттерны убытков
- лучшие условия для входа
- проблемы риск менеджмента
- психологические ошибки


История:

{trades}


Ответь как профессиональный трейдинг наставник.

Структура:

📊 Общая статистика

❌ Главные ошибки

✅ Что работает

🧠 Психология

🎯 Что изменить

"""


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )


    return response.choices[0].message.content

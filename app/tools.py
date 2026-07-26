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

def market_brief_tool(user_id):

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
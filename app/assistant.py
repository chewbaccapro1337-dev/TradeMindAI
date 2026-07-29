from journal import show_statistics
from ai import ask_ai, extract_profile
from database import save_ai_message, get_ai_memory, get_profile, update_trader_profile, get_last_trades_for_ai
import json
from ai import client
from tools import (
    btc_analysis_tool,
    statistics_tool,
    last_trades_tool,
    news_tool,
    market_brief_tool,
    create_trade_tool,
    close_trade_tool,
    trade_copilot_tool
)

TOOLS = {

    "btc_analysis": btc_analysis_tool,

    "statistics": statistics_tool,

    "last_trades": last_trades_tool,

    "news": news_tool,
    
    "market_brief": market_brief_tool,

    "create_trade": create_trade_tool,

    "close_trade": close_trade_tool,

    "trade_copilot": trade_copilot_tool,

}

def process_message(user_id, text: str):

    from profile_ai import extract_profile
    from database import update_trader_profile


    profile_data = extract_profile(text)


    for field,value in profile_data.items():

        if value:

            update_trader_profile(
                user_id,
                field,
                value
            )

    action = detect_action(text)

    print("DETECTED ACTION:", action)


    tool = TOOLS.get(
     action["action"]
    )

    print("ACTION:", action)
    print("AVAILABLE TOOLS:", TOOLS.keys())
    print("TOOL FOUND:", tool)

    if tool:

        print(
         "RUN TOOL:",
         action["action"]
    )

        if action["action"] == "news":
         return tool(
               user_id,
               action.get("symbol")
            )

        elif action["action"] == "market_brief":
            return tool(
                user_id,
                action.get("symbol"),
                action.get("market")
            )

        elif action["action"] == "create_trade":
            return tool(
                user_id,
                text
            )

        elif action["action"] == "close_trade":
            return tool(
                user_id,
                text
            )

        else:
            return tool(
                user_id
            )

    if not tool:

        print(
         "NO TOOL. GO TO AI MEMORY"
        )
 
    # сохраняем вопрос пользователя
    save_ai_message(
        user_id,
        "user",
        text
    )


    # достаем память
    memory = get_ai_memory(
        user_id,
        limit=10
    )


    # извлекаем профиль
    profile_data = extract_profile(text)


    for field, value in profile_data.items():

        if value:

            update_trader_profile(
                user_id,
                field,
                value
            )


    profile = get_profile(
        user_id
    )

    trades = get_last_trades_for_ai(
        user_id,
        10
    )

    # отправляем в AI
    response = ask_ai(
        text,
        memory,
        profile
    )


    # сохраняем ответ
    save_ai_message(
        user_id,
        "assistant",
        response
    )


    return response

def detect_action(text):

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": """
Ты — Router AI внутри TradeMind AI.

Твоя задача:
Определить намерение пользователя и выбрать ОДНО действие.

Возвращай ТОЛЬКО JSON.

Формат:

{
"action":"название"
}


ПРАВИЛА ПРИОРИТЕТА:

1. CREATE TRADE — самый высокий приоритет.

Выбирай create_trade если сообщение содержит:
- открыть сделку
- записать сделку
- добавить сделку
- сохранить сделку
- вход
- BUY/SELL/LONG/SHORT
- BTC/EURUSD и цены
- SL/TP/риск внутри описания сделки

ВАЖНО:
Слова:
"риск"
"стоп"
"тейк"
"вход"

НЕ являются risk, если пользователь описывает сделку.


Пример:

"BTC BUY вход 65000 SL 64000 TP 67000 риск 50"

Ответ:

{
"action":"create_trade"
}



2. CLOSE TRADE

Только если пользователь хочет закрыть позицию.

Фразы:

"закрой сделку"
"закрыть последнюю"
"я вышел"
"закрыл BTC"
"закрыл позицию"

Ответ:

{
"action":"close_trade"
}



3. LAST TRADES

Если пользователь хочет посмотреть историю:

"последние сделки"
"покажи сделки"
"мои сделки"
"история сделок"

Ответ:

{
"action":"last_trades"
}



4. TRADE COACH

Если пользователь хочет обучение:

"разбери мои ошибки"
"почему я слил"
"улучши мою торговлю"
"мой коуч"

Ответ:

{
"action":"trade_coach"
}



5. TRADE ANALYSIS

Если пользователь отправил конкретную сделку и хочет её анализ:

"проанализируй сделку"
"разбор сделки"
"ошибка входа"

Ответ:

{
"action":"trade_analysis"
}



6. MARKET BRIEF

Общий обзор рынка.

Крипта:

"что по BTC"
"что по битку"
"обзор крипты"

Ответ:

{
"action":"market_brief",
"market":"crypto",
"symbol":"BTCUSDT"
}


Форекс:

"что по EURUSD"
"обзор евро"
"что по GBPUSD"

Ответ:

{
"action":"market_brief",
"market":"forex",
"symbol":"EURUSD"
}



7. NEWS

Новости:

"новости"
"календарь"
"CPI"
"FOMC"
"NFP"
"инфляция"

Ответ:

{
"action":"news",
"symbol":null
}



8. RISK

ТОЛЬКО отдельный расчёт.

Примеры:

"посчитай риск"
"какой размер позиции"
"сколько лотов"

НЕ использовать если есть:
BUY/SELL/LONG/SHORT
ENTRY/SL/TP


Ответ:

{
"action":"risk"
}



9. STATISTICS

Если:

"статистика"
"моя статистика"
"процент побед"


Ответ:

{
"action":"statistics"
}



10. PROFILE

Если:

"кто я"
"мой профиль"


Ответ:

{
"action":"profile"
}



11. MEMORY

Если:

"что ты помнишь"


Ответ:

{
"action":"memory"
}



12. CHAT

Все остальные сообщения.

Ответ:

{
"action":"chat"
}



Проверяй сообщение сверху вниз.
Первое подходящее правило имеет приоритет.

Не объясняй.
Не добавляй текст.
Только JSON.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )

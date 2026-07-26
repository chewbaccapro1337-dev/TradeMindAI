from journal import show_statistics
from ai import ask_ai, extract_profile
from database import save_ai_message, get_ai_memory, get_profile, update_profile, get_last_trades_for_ai
import json
from ai import client
from tools import (
    btc_analysis_tool,
    statistics_tool,
    last_trades_tool,
    news_tool,
    market_brief_tool
)

TOOLS = {

    "btc_analysis": btc_analysis_tool,

    "statistics": statistics_tool,

    "last_trades": last_trades_tool,

    "news": news_tool,
    
    "market_brief": market_brief_tool

}

def process_message(user_id, text: str):

    text_lower = text.lower()

    action = detect_action(text)

    tool = TOOLS.get(
        action["action"]
    )
    if tool:
        return tool(user_id)

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


    # извлекаем информацию о пользователе
    profile_data = extract_profile(text)

    

    # сохраняем найденные данные
    for field, value in profile_data.items():

        if value:

            update_profile(
                user_id,
                field,
                value
            )


    # получаем профиль
    profile = get_profile(
        user_id
    )

    trades = get_last_trades_for_ai(
     user_id,
     10
    )

    # отправляем запрос AI
    response = ask_ai(
        text,
        memory,
        profile,
        trades
    )


    # сохраняем ответ AI
    save_ai_message(
        user_id,
        "assistant",
        response
    )


    return response

def detect_action(text):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": """
Ты управляющий модуль TradeMind AI.

Твоя задача определить, какой инструмент нужно использовать.

Верни только JSON.

Формат:

{
"action":"..."
}

Доступные действия:

btc_analysis
если пользователь хочет анализ BTC, ETH, рынка, графика, структуры рынка, тренда.

statistics
если пользователь хочет общую статистику торговли.

last_trades
если пользователь хочет увидеть последние сделки, последнюю сделку, историю сделок.

trade_coach
если пользователь хочет анализ своих ошибок, улучшение торговли, разбор своих сделок

news
если пользователь спрашивает:
- новости
- календарь
- важные события
- CPI
- FOMC
- NFP
- инфляция

market_brief

если пользователь спрашивает:
- что по рынку сегодня
- дай обзор рынка
- план на сегодня
- что сейчас происходит
- стоит ли торговать сегодня

risk
если пользователь хочет рассчитать риск или размер позиции.

trade_analysis
если пользователь хочет проанализировать сделку.

profile
если спрашивает информацию о себе.

memory
если спрашивает что ты помнишь.

chat
для всех остальных сообщений.

Ничего кроме JSON не выводи.

"""
            },
            {
                "role":"user",
                "content":text
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )
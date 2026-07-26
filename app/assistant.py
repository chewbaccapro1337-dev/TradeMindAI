from journal import show_statistics
from ai import ask_ai, extract_profile
from database import save_ai_message, get_ai_memory, get_profile, update_profile
import json
from ai import client


def process_message(user_id, text: str):

    text_lower = text.lower()

    action = detect_action(text)


    if action["action"] == "btc_analysis":

        from analysis import make_report

        return make_report()


    if action["action"] == "statistics":

        return "Статистика пока в разработке."


        if action["action"] == "news":

        return "Новости пока в разработке."

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


    # отправляем запрос AI
    response = ask_ai(
        text,
        memory,
        profile
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

Определи действие пользователя.

Верни JSON:

{
"action":"..."
}

Доступные действия:

btc_analysis -
если нужен анализ BTC

statistics -
если нужна статистика

news -
если нужны новости

chat -
обычный разговор

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
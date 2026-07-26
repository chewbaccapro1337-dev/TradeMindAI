from journal import show_statistics
from ai import ask_ai
from database import save_ai_message, get_ai_memory


def process_message(user_id, text: str):

    text_lower = text.lower()

    if "btc" in text_lower or "битк" in text_lower:
        from analysis import make_report
        return make_report()

    if "стат" in text_lower:
        return "Статистика пока в разработке."

    if "новост" in text_lower:
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


    # отправляем AI вместе с историей
    response = ask_ai(
        text,
        memory
    )


    # сохраняем ответ AI
    save_ai_message(
        user_id,
        "assistant",
        response
    )


    return response
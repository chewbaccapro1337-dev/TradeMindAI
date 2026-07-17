from telegram import Update
from telegram.ext import ContextTypes
import requests
from keyboards import main_keyboard
from economic_calendar import get_calendar
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from forex_news import get_news


# Главное меню новостей
async def show_news(update, context):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 High Impact",
                callback_data="news_high"
            )
        ],
        [
            InlineKeyboardButton(
                "💵 USD",
                callback_data="news_usd"
            ),
            InlineKeyboardButton(
                "💶 EUR",
                callback_data="news_eur"
            )
        ],
        [
            InlineKeyboardButton(
                "💷 GBP",
                callback_data="news_gbp"
            )
        ],
        [
            InlineKeyboardButton(
                "📅 Все новости",
                callback_data="news_all"
            )
        ]
    ]


    await update.message.reply_text(
        "📰 Экономический календарь\n\nВыбери фильтр:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# Обработка кнопок
async def news_button(update, context):

    query = update.callback_query
    await query.answer()


    if query.data == "news_high":
        events = get_news(only_high=True)

    elif query.data == "news_usd":
        events = get_news(currency="USD")

    elif query.data == "news_eur":
        events = get_news(currency="EUR")

    elif query.data == "news_gbp":
        events = get_news(currency="GBP")

    else:
        events = get_news()


    if not events:
        await query.edit_message_text(
            "📰 Новостей не найдено."
        )
        return


    text = "📰 Экономический календарь\n\n"


    for e in events[:20]:

        if e["impact"] == "red":
            icon = "🔴"

        elif e["impact"] == "orange":
            icon = "🟠"

        else:
            icon = "⚪"


        text += (
            f"{icon} {e['currency']}\n"
            f"⏰ {e['time']} МСК\n"
            f"{e['event']}\n"
        )


        if e.get("forecast"):
            text += f"📊 Прогноз: {e['forecast']}\n"

        if e.get("previous"):
            text += f"◽ Предыдущее: {e['previous']}\n"

        if e.get("actual"):
            text += f"✅ Факт: {e['actual']}\n"


        text += "\n━━━━━━━━━━━━━━\n"


    await query.edit_message_text(
        text[:4000]
    )

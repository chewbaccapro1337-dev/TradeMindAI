from telegram import Update
from telegram.ext import ContextTypes
import requests
from keyboards import main_keyboard
from economic_calendar import get_calendar
from forex_news import get_news

async def show_news(update, context):

    events = get_news()

    if not events:
        await update.message.reply_text(
            "📰 Сегодня важных новостей нет."
        )
        return

    text = "📰 Экономический календарь\n\n"

    for e in events:

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

        if e["forecast"]:
            text += f"📊 Прогноз: {e['forecast']}\n"

        if e["actual"]:
            text += f"✅ Факт: {e['actual']}\n"

        text += "\n━━━━━━━━━━━━━━\n"

    await update.message.reply_text(
        text[:4000]
    )

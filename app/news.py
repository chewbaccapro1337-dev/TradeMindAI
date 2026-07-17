from telegram import Update
from telegram.ext import ContextTypes
import requests
from keyboards import main_keyboard
from calendar import get_calendar

async def show_news(update, context):

    data = get_calendar()

    await update.message.reply_text(str(data))


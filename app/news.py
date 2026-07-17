from telegram import Update
from telegram.ext import ContextTypes

from keyboards import main_keyboard


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🧠 TRADEMIND AI
═══════════════════

📰 ЭКОНОМИЧЕСКИЙ КАЛЕНДАРЬ

⏳ Загружаю новости...

═══════════════════

🤖 TradeMind AI
"""

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard
    )
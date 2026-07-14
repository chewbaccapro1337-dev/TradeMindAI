from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

SYMBOL, SIDE, ENTRY, EXIT = range(2, 6)

journal_data = {}


async def ask_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Введите инструмент.\n\nНапример:\nBTCUSDT"
    )

    return SYMBOL
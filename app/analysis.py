from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import back_keyboard, main_keyboard
import os
from ai import analyze_trade

ANALYZE = 20

async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Отправьте скриншот сделки.",
        reply_markup=back_keyboard
    )

    return ANALYZE

async def analyze_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Отправьте изображение."
        )
        return ANALYZE

    print("Фото получено")

    await update.message.reply_text("🔍 Анализирую сделку...")

    photo = update.message.photo[-1]
    file = await photo.get_file()

    os.makedirs("photos", exist_ok=True)

    file_path = f"photos/{update.effective_user.id}.jpg"

    await file.download_to_drive(file_path)

    await update.message.reply_text(
        "🤖 Анализирую график..."
    )

    result = analyze_trade(file_path)

    await update.message.reply_text(
        result,
        reply_markup=main_keyboard
    )

    return ConversationHandler.END
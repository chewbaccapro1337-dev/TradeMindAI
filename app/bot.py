from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)
from dotenv import load_dotenv
import os
from risk import calculate_risk
from database import create_tables

# Загружаем переменные из .env
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

BALANCE, RISK = range(2)

BOT_NAME = "TradeMind_AI"
VERSION = "0.1.0"

# Временное хранилище данных пользователей
user_data = {}

keyboard = [
    ["📊 Рассчитать риск"],
    ["📈 Журнал сделок"],
    ["📷 Анализ сделки"],
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Добро пожаловать в TradeMind AI!\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance = float(context.args[0])
        risk_percent = float(context.args[1])

        risk_amount = calculate_risk(balance, risk_percent)

        await update.message.reply_text(
            f"💰 Баланс: ${balance:.2f}\n"
            f"📉 Риск: {risk_percent}%\n"
            f"⚠️ Максимальный убыток: ${risk_amount:.2f}"
        )

    except (IndexError, ValueError):
        await update.message.reply_text(
            "Использование:\n"
            "/risk <баланс> <риск>\n\n"
            "Пример:\n"
            "/risk 1200 0.5"
        )

async def ask_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Введите баланс:")
    return BALANCE

async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance = float(update.message.text)

        user_data[update.effective_user.id] = {
            "balance": balance
        }

        await update.message.reply_text(
            "📉 Теперь введите риск (%):"
        )

        return RISK

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число.\nНапример:\n1200"
        )

        return BALANCE

async def get_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        risk_percent = float(update.message.text)

        balance = user_data[update.effective_user.id]["balance"]

        risk_amount = calculate_risk(balance, risk_percent)

        await update.message.reply_text(
            f"💰 Баланс: ${balance:.2f}\n"
            f"📉 Риск: {risk_percent}%\n"
            f"⚠️ Максимальный риск: ${risk_amount:.2f}",
            reply_markup=reply_markup
        )

        user_data.pop(update.effective_user.id, None)

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число.\nНапример:\n0.5"
        )

        return RISK

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    create_tables()

    print(f"🤖 {BOT_NAME} v{VERSION} запущен!")

    conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("risk", ask_balance),
        MessageHandler(filters.Regex("^📊 Рассчитать риск$"), ask_balance),
    ],
    states={
        BALANCE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_balance)
        ],
        RISK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_risk)
        ],
    },
    fallbacks=[],
    
)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()
if __name__ == "__main__":
    main()
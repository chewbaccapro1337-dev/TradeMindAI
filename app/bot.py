from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from risk import calculate_risk

# Загружаем переменные из .env
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я TradeMind AI.\n\n"
        "Скоро я научусь:\n"
        "• считать риск\n"
        "• вести журнал сделок\n"
        "• анализировать сделки"
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

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("risk", risk))

    print("🤖 Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
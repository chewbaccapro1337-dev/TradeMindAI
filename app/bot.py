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
from journal import (
    ask_symbol,
    get_symbol,
    get_side,
    get_entry,
    get_tp,
    get_sl,
    get_exit,
    get_trade_risk,
    back,
    show_last_trades,
    show_statistics
)
from keyboards import (
    main_keyboard,
    back_keyboard,
    start_keyboard
)
from telegram import ReplyKeyboardRemove
from session import session_data
from analysis import (
    ask_photo,
    analyze_photo,
    ANALYZE,
)
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest
from news import show_news, news_button
from telegram.ext import CallbackQueryHandler
from states import (
    BALANCE,
    RISK,
    SYMBOL,
    SIDE,
    ENTRY,
    TP,
    SL,
    TRADE_RISK,
    POSITION_SIZE,
    COMMENT,
    ANALYZE
)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")

BOT_NAME = "TradeMind_AI"
VERSION = "1.0.1"

# Временное хранилище данных пользователей

RISK_BACK_MENU = "menu"
RISK_BACK_BALANCE = "balance"

reply_markup=main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text(
     "Пока я умею:\n"
     "• 📊 Рассчитывать риск\n"
     "• 📝 Записывать сделки\n"
     "• 📄 Отображать последние сделки\n\n"
     "🚀 Скоро появится много новых функций!\n\n"
     "Нажмите «🚀 Старт», чтобы открыть главное меню.",
     reply_markup=start_keyboard
 )

async def open_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Главное меню",
        reply_markup=main_keyboard
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
    context.user_data["module"] = "risk"
    context.user_data["back"] = "menu"

    await update.message.reply_text(
        "💰 Введите баланс:",
        reply_markup=back_keyboard
    )

    return BALANCE

async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance = float(update.message.text)

        context.user_data["balance"] = balance
        context.user_data["back"] = "balance"

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

        balance = context.user_data["balance"]

        risk_amount = calculate_risk(balance, risk_percent)

        await update.message.reply_text(
            f"💰 Баланс: ${balance:.2f}\n"
            f"📉 Риск: {risk_percent}%\n"
            f"⚠️ Максимальный риск: ${risk_amount:.2f}",
            reply_markup=reply_markup
        )

        context.user_data.clear()

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число.\nНапример:\n0.5"
        )

        return RISK

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("CANCEL CALLED")
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Действие отменено.",
        reply_markup=ReplyKeyboardRemove()
    )

    await update.message.reply_text(
        "🏠 Главное меню",
        reply_markup=main_keyboard
    )

    return ConversationHandler.END

def main():

    proxy_url = "socks5://qMLzj4:r5NZWQ@168.81.42.247:8000"

    request = HTTPXRequest(
        proxy=proxy_url,
        connect_timeout=30,
        read_timeout=60,
        write_timeout=30,
        pool_timeout=30
    )

    get_updates_request = HTTPXRequest(
        proxy=proxy_url,
        connect_timeout=30,
        read_timeout=90,
        write_timeout=30,
        pool_timeout=30
    )
    app = ( ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .get_updates_request(get_updates_request)
        .build()
    )
    create_tables()

    print(f"🤖 {BOT_NAME} v{VERSION} запущен!")

    conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("risk", ask_balance),
        MessageHandler(filters.Regex("^📊 Рассчитать риск$"), ask_balance),
        MessageHandler(filters.Regex("^📝 Записать сделку$"), ask_symbol),
        MessageHandler(filters.Regex("^📷 Анализ сделки$"), ask_photo),
    ],
    states={
        BALANCE: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_balance
        )
     ],
        RISK: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
	            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_risk
        )
     ],
        SYMBOL: [
    MessageHandler(
        filters.TEXT
        & ~filters.COMMAND
        & ~filters.Regex("^⬅️ Назад$")
        & ~filters.Regex("^❌ Отмена$"),
        get_symbol
    )
     ],
      SIDE: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_side
        )
     ],
    ENTRY: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_entry
        )
     ],
    TP: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_tp
        ) 
     ],

    SL: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            get_sl
        )
     ],
 TRADE_RISK: [
        MessageHandler(
           filters.TEXT
           & ~filters.COMMAND
           & ~filters.Regex("^⬅️ Назад$")
           & ~filters.Regex("^❌ Отмена$"),
           get_trade_risk
    )  
     ],

 ANALYZE: [
        MessageHandler(
          filters.PHOTO,
          analyze_photo
    )
     ],
    },
  fallbacks=[
    CommandHandler("cancel", cancel),
    MessageHandler(filters.Regex("^❌ Отмена$"), cancel),
    MessageHandler(filters.Regex("^⬅️ Назад$"), back),
]
)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
    MessageHandler(
        filters.Regex("^🚀 Старт$"),
        open_main_menu
    )
)
    app.add_handler(
    MessageHandler(
        filters.Regex("^📒 Последние сделки$"),
        show_last_trades
    )
)

    app.add_handler(
    MessageHandler(
        filters.Regex("📈 Статистика"),
        show_statistics
    )
)
    app.add_handler(
    MessageHandler(
        filters.Regex("^📰 Новости$"),
        show_news
    )
)
    app.add_handler(
    CallbackQueryHandler(news_button)
)



    app.add_handler(conv_handler)

    app.add_handler(CommandHandler("start", start))

    app.run_polling(
       timeout=60,
       drop_pending_updates=False
)
if __name__ == "__main__":
    main()

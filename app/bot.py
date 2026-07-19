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
    show_statistics,
    start_close_trade,
    select_close_trade,
    close_trade_price,
    clear_history
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
    analyze_market,
    make_report
)
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest
from news import show_news, news_button
from subscription_menu import subscription, buy_callback, receive_payment
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
    ANALYZE,
    SELECT_CLOSE_TRADE,
    CLOSE_PRICE
)
from liquidity_report import make_report
from subscription import has_subscription
from database import add_subscription
from admin import users, grant, revoke
from analysis import analyze_market

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
        "🚀 Добро пожаловать в TradeMind AI!\n\n"
        "🎁 Новым пользователям предоставлен тестовый период 1 день\n\n"
        "Доступные функции:\n"
        "📊 Журнал сделок\n"
        "📰 Экономический календарь\n"
        "🤖 AI анализ новостей\n"
        "🧠 AI Анализ BTC\n",
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

async def show_liquidity(update, context):

    print("КНОПКА AI АНАЛИЗ НАЖАТА")

    await update.message.reply_text(
        "⏳ Анализирую рынок..."
    )

    report =  report = make_report()

    await update.message.reply_text(report)

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
        MessageHandler(filters.Regex("^📝 Записать сделку$"), ask_symbol),
        MessageHandler(filters.Regex("^🔒 Закрыть$"), start_close_trade),
        MessageHandler(filters.Regex("^📷 AI Анализ$"), ask_photo),
        MessageHandler(filters.Regex("^💎 Подписка$"), subscription)
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
 SELECT_CLOSE_TRADE: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            select_close_trade
        )
     ],
	
 CLOSE_PRICE: [
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & ~filters.Regex("^⬅️ Назад$")
            & ~filters.Regex("^❌ Отмена$"),
            close_trade_price
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
        filters.Regex("^📒 Сделки$"),
        show_last_trades
    )
)

    app.add_handler(
    MessageHandler(
        filters.Regex("🧠 AI BTC"),
        show_liquidity
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
        filters.Regex("^🗑 Очистить историю$"),
        clear_history
    )
)

    app.add_handler(
    MessageHandler(
        filters.Regex("^📰 Новости$"),
        show_news
    )
)
    app.add_handler(
    CallbackQueryHandler(
        news_button,
        pattern="^news_"
    )
)

    app.add_handler(
    CallbackQueryHandler(
        buy_callback,
        pattern="^buy_"
    )
)

    app.add_handler(
    MessageHandler(
        filters.Document.PDF,
        receive_payment
    )
)

    app.add_handler(conv_handler)

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("revoke", revoke))

    app.add_handler(
    CommandHandler(
        "subscription",
        subscription
    )
)

    app.run_polling(
       timeout=60,
       drop_pending_updates=False
)
if __name__ == "__main__":
    main()

async def market_analysis(update, context):

    data = analyze_market()


    text = f"""
📊 BTC ANALYSIS

Тренд:
{data['trend']}


Цена:
{data['price']}


Структура:
{data['bos_choch']}


Ликвидность:
{data['sweep']}


Зона интереса:
{data['entry_zone']}


Сигнал:
{data['signal']}
"""


    await update.message.reply_text(
        text
    )
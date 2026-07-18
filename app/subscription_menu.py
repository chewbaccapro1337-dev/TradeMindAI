from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from subscription import check_subscription


async def subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    active = check_subscription(user_id)


    if active:
        status = "🟢 Активна"
    else:
        status = "🔴 Завершена"


    keyboard = [
        [
            InlineKeyboardButton(
                "💎 7 дней — 299₽",
                callback_data="buy_7"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 30 дней — 799₽",
                callback_data="buy_30"
            )
        ],
        [
            InlineKeyboardButton(
                "🔥 Навсегда — 4990₽",
                callback_data="buy_forever"
            )
        ]
    ]


    await update.message.reply_text(
        f"""
💎 TradeMind AI Premium

Статус:
{status}


Что входит:

🤖 AI анализ сделок
📰 AI анализ новостей
💧 Liquidity Map
📊 Статистика торговли
📈 Журнал сделок


Выберите тариф:
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "buy_7":
        days = 7
        price = 299

    elif query.data == "buy_30":
        days = 30
        price = 799

    elif query.data == "buy_forever":
        days = 36500
        price = 4990


    await query.message.reply_text(
        f"""
💎 TradeMind AI Premium

Вы выбрали:
📅 {days} дней
💰 Стоимость: {price}₽


Оплата только:

🏦 Альфа-Банк

💳 Карта:
2200154519151905


📱 СБП:
+7-908-128-68-26


После оплаты отправьте сюда PDF чек.

После проверки подписка будет активирована.
"""
    )

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from subscription import check_subscription
from news_cache import update_news
from news_cache import get_cached_news

async def show_news(update, context):

    if not check_subscription(update.effective_user.id):

        await update.message.reply_text(
            "🔒 Тестовый доступ закончился.\n\n"
            "TradeMind AI Premium:\n"
            "🤖 AI анализ\n"
            "📰 Новости\n"
            "💧 Liquidity Map\n\n"
            "Для продолжения оформите подписку."
        )

        return


    # обновляем кэш (если старый больше часа — качает новые)
    update_news()


    keyboard = [
        [
            InlineKeyboardButton(
                "🔴 High Impact",
                callback_data="news_high"
            )
        ],
        [
            InlineKeyboardButton(
                "💵 USD",
                callback_data="news_usd"
            ),
            InlineKeyboardButton(
                "💶 EUR",
                callback_data="news_eur"
            )
        ],
        [
            InlineKeyboardButton(
                "💷 GBP",
                callback_data="news_gbp"
            )
        ],
        [
            InlineKeyboardButton(
                "📅 Все новости",
                callback_data="news_all"
            )
        ],
        [
            InlineKeyboardButton(
                "🤖 AI анализ",
                callback_data="news_ai"
            )
        ]
    ]


    await update.message.reply_text(
        "📰 Экономический календарь\n\nВыбери фильтр:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def news_button(update, context):

    query = update.callback_query
    await query.answer()


    events = get_cached_news()


    if query.data == "news_high":

        events = [
            e for e in events
            if e.get("impact") == "red"
        ]


    elif query.data == "news_usd":

        events = [
            e for e in events
            if e.get("currency") == "USD"
        ]


    elif query.data == "news_eur":

        events = [
            e for e in events
            if e.get("currency") == "EUR"
        ]


    elif query.data == "news_gbp":

        events = [
            e for e in events
            if e.get("currency") == "GBP"
        ]


    elif query.data == "news_ai":

        events = events[:10]


    if not events:

        await query.edit_message_text(
            "📭 Новостей нет."
        )

        return



    text = "📰 Экономический календарь\n\n"


    for e in events[:10]:

        impact = "🔴" if e.get("impact") == "red" else "🟡"

        text += (
            f"{impact} {e.get('currency')}\n"
            f"📌 {e.get('title')}\n"
            f"🕒 {e.get('time')}\n\n"
        )


    await query.edit_message_text(
        text[:4000]
    )
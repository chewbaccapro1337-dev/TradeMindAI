from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from subscription import check_subscription

from news_cache import get_cached_news
from economic_calendar import get_calendar



async def show_news(update, context):

    if not check_subscription(update.effective_user.id):

        await update.message.reply_text(
            "🔒 Тестовый доступ закончился.\n\n"
            "TradeMind AI Premium:\n"
            "🤖 AI анализ\n"
            "📰 Новости\n"
            "💧 BTC AI\n\n"
            "Для продолжения оформите подписку."
        )

        return


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


    # =========================
    # Все новости
    # =========================

    if query.data == "news_all":

        events = get_cached_news()

        title = "📰 Последние новости\n\n"



    # =========================
    # Экономический календарь
    # =========================

    else:

        events = get_calendar()

        title = "📅 Экономический календарь\n\n"



    # =========================
    # Фильтры
    # =========================


    if query.data == "news_high":

        events = [
            e for e in events
            if e.get("impact") == "red"
        ]

        title = "🔴 HIGH IMPACT EVENTS\n\n"



    elif query.data == "news_usd":

        events = [
            e for e in events
            if e.get("currency") == "USD"
        ]

        title = "💵 USD ECONOMIC CALENDAR\n\n"



    elif query.data == "news_eur":

        events = [
            e for e in events
            if e.get("currency") == "EUR"
        ]

        title = "💶 EUR ECONOMIC CALENDAR\n\n"



    elif query.data == "news_gbp":

        events = [
            e for e in events
            if e.get("currency") == "GBP"
        ]

        title = "💷 GBP ECONOMIC CALENDAR\n\n"



    elif query.data == "news_ai":

        events = get_calendar()

        title = "🤖 AI ECONOMIC ANALYSIS\n\n"




    if not events:

        await query.edit_message_text(
            "📭 Событий нет."
        )

        return




    text = title



    for e in events[:10]:

        if e.get("impact") == "red":

            impact = "🔴 HIGH"

        elif e.get("impact") == "orange":

            impact = "🟠 MEDIUM"

        else:

            impact = "🟡 LOW"



        text += (

            f"{impact}\n"
            f"🌍 {e.get('currency')}\n"
            f"🕒 {e.get('time')}\n"
            f"📌 {e.get('title')}\n\n"

        )



    await query.edit_message_text(
        text[:4000]
    )
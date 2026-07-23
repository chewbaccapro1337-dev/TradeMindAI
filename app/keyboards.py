from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(
    [
        ["🚀 Старт"]
    ],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    [
        ["📷 AI Анализ", "🧠 AI BTC"],
        ["📝 Записать сделку"],
        ["📒 Сделки", "📈 Статистика", "🔒 Закрыть"],
        ["🗑 Очистить историю"],
        ["📰 Новости"],
        ["💎 Подписка"]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    [
        ["⬅️ Назад", "❌ Отмена"]
    ],
    resize_keyboard=True
)

buy_sell_keyboard = ReplyKeyboardMarkup(
    [
        ["🟢 BUY", "🔴 SELL"],
        ["⬅️ Назад", "❌ Отмена"]
    ],
    resize_keyboard=True
)

symbol_keyboard = ReplyKeyboardMarkup(
    [
        ["BTCUSDT", "ETHUSDT"],
        ["EURUSD", "GBPUSD"],
        ["⬅️ Назад", "❌ Отмена"],
    ],
    resize_keyboard=True
)

currency_keyboard = ReplyKeyboardMarkup(
    [
        ["💵 USD", "₽ RUB"],
        ["⬅️ Назад"]
    ],
    resize_keyboard=True
)
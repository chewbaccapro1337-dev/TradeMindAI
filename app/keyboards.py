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
        ["📊 Рассчитать риск"],
        ["📝 Записать сделку"],
        ["📒 Последние сделки", "📈 Статистика"],
        ["🔒 Закрыть сделку"],
        ["🗑 Очистить историю"],
        ["📷 Анализ сделки"],
        ["📰 Новости"]
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

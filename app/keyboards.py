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
        ["📈 Журнал сделок"],
        ["📄 Последние сделки"],
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
        ["SOLUSDT", "BNBUSDT"],
        ["⬅️ Назад", "❌ Отмена"],
    ],
    resize_keyboard=True
)
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import get_last_trades
from keyboards import (
    main_keyboard,
    back_keyboard,
    buy_sell_keyboard,
    symbol_keyboard,
)
from database import save_trade
from session import session_data

SYMBOL, SIDE, ENTRY, EXIT, TRADE_RISK = range(10, 15)

trade_data = session_data

BACK_TO_MENU = "menu"
BACK_TO_SYMBOL = "symbol"
BACK_TO_SIDE = "side"
BACK_TO_ENTRY = "entry"

async def ask_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trade_data[update.effective_user.id] = {
        "module": "journal",
        "back": BACK_TO_MENU
    }

    await update.message.reply_text(
        "📈 Выберите инструмент:",
        reply_markup=symbol_keyboard
    )

    return SYMBOL
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # ---------------- Журнал сделок ----------------

    if user_id in trade_data:

        back_state = trade_data[user_id]["back"]

        if back_state == BACK_TO_MENU:
            trade_data.pop(user_id, None)

            await update.message.reply_text(
                "🏠 Главное меню",
                reply_markup=main_keyboard
            )

            return ConversationHandler.END

        elif back_state == BACK_TO_SYMBOL:

            trade_data[user_id]["back"] = BACK_TO_MENU

            await update.message.reply_text(
                "📈 Выберите инструмент:",
                reply_markup=symbol_keyboard
            )

            return SYMBOL

        elif back_state == BACK_TO_SIDE:

            trade_data[user_id]["back"] = BACK_TO_SYMBOL

            await update.message.reply_text(
                "Выберите направление:",
                reply_markup=buy_sell_keyboard
            )

            return SIDE

        elif back_state == BACK_TO_ENTRY:

            trade_data[user_id]["back"] = BACK_TO_SIDE

            await update.message.reply_text(
                "💵 Введите цену входа:",
                reply_markup=back_keyboard
            )

            return ENTRY

    # ---------------- Расчет риска ----------------

    if context.user_data.get("module") == "risk":

        back = context.user_data.get("back")

        if back == "menu":

            context.user_data.clear()

            await update.message.reply_text(
                "🏠 Главное меню",
                reply_markup=main_keyboard
            )

            return ConversationHandler.END

        elif back == "balance":

            context.user_data["back"] = "menu"

            await update.message.reply_text(
                "💰 Введите баланс:",
                reply_markup=back_keyboard
            )

            return 0
async def get_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in trade_data:
        trade_data[user_id] = {
            "module": "journal",
            "back": BACK_TO_MENU,
        }

    trade_data[user_id]["symbol"] = update.message.text.upper()
    trade_data[user_id]["back"] = BACK_TO_SYMBOL

    await update.message.reply_text(
        "Выберите направление:",
        reply_markup=buy_sell_keyboard
    )

    return SIDE

async def get_side(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "Отмена" in update.message.text:
        trade_data.pop(update.effective_user.id, None)

        await update.message.reply_text(
            "❌ Действие отменено.",
            reply_markup=main_keyboard
        )

        return ConversationHandler.END

    side = update.message.text

    if side == "🟢 BUY":
        side = "BUY"
    elif side == "🔴 SELL":
        side = "SELL"
    else:
        await update.message.reply_text(
            "❌ Используйте кнопки BUY или SELL.",
            reply_markup=buy_sell_keyboard
        )
        return SIDE

    trade_data[update.effective_user.id]["side"] = side

    await update.message.reply_text(
        "💵 Введите цену входа:",
        reply_markup=back_keyboard
    )

    return ENTRY
   

    
async def get_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "Отмена" in update.message.text:
        trade_data.pop(update.effective_user.id, None)

        await update.message.reply_text(
            "❌ Действие отменено.",
            reply_markup=main_keyboard
        )

        return ConversationHandler.END

    try:
        entry = float(update.message.text)

        trade_data[update.effective_user.id]["entry"] = entry

        await update.message.reply_text(
    "💰 Введите цену выхода:",
    reply_markup=back_keyboard
)
        trade_data[update.effective_user.id]["back"] = BACK_TO_ENTRY
        return EXIT

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число.\nНапример:\n108000"
        )

        return ENTRY



async def get_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "Отмена" in update.message.text:
        trade_data.pop(update.effective_user.id, None)

        await update.message.reply_text(
            "❌ Действие отменено.",
            reply_markup=main_keyboard
        )

        return ConversationHandler.END

    try:
        exit_price = float(update.message.text)

        user = trade_data[update.effective_user.id]

        user["exit"] = exit_price
        trade_data[update.effective_user.id]["exit"] = exit_price

        await update.message.reply_text(
         "💵 Введите риск сделки ($):",
         reply_markup=back_keyboard
        )

        return TRADE_RISK

        pnl = (
            exit_price - user["entry"]
            if user["side"] == "BUY"
            else user["entry"] - exit_price
        )

        save_trade(
            user_id=update.effective_user.id,
            symbol=user["symbol"],
            side=user["side"],
            entry=user["entry"],
            exit_price=exit_price,
            risk=0,
            pnl=pnl,
        )

        await update.message.reply_text(
            "✅ Сделка сохранена!\n\n"
            f"📈 {user['symbol']}\n"
            f"📊 {user['side']}\n"
            f"💵 PnL: {pnl:.2f}",
            reply_markup=main_keyboard
        )

        trade_data.pop(update.effective_user.id, None)

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("❌ Введите число.")

        return EXIT
async def get_trade_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        risk = float(update.message.text)

        user = trade_data[update.effective_user.id]

        user["risk"] = risk

        pnl = (
            user["exit"] - user["entry"]
            if user["side"] == "BUY"
            else user["entry"] - user["exit"]
        )

        r_multiple = pnl / risk if risk != 0 else 0

        save_trade(
            user_id=update.effective_user.id,
            symbol=user["symbol"],
            side=user["side"],
            entry=user["entry"],
            exit_price=user["exit"],
            risk=risk,
            pnl=pnl,
        )

        await update.message.reply_text(
            "✅ Сделка сохранена!\n\n"
            f"📈 {user['symbol']}\n"
            f"📊 {user['side']}\n"
            f"💵 PnL: {pnl:.2f}$\n"
            f"⚠️ Риск: {risk:.2f}$\n"
            f"🎯 R: {r_multiple:.2f}",
            reply_markup=main_keyboard
        )

        trade_data.pop(update.effective_user.id, None)

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число."
        )

        return TRADE_RISK
async def show_last_trades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trades = get_last_trades(update.effective_user.id)

    if not trades:
        await update.message.reply_text(
            "📭 У вас пока нет сохранённых сделок."
        )
        return

    text = "📄 Последние сделки:\n\n"

    for i, trade in enumerate(trades, start=1):
        symbol, side, entry, exit_price, pnl, created = trade

        text += (
            f"{i}. {symbol} | {side}\n"
            f"Вход: {entry}\n"
            f"Выход: {exit_price}\n"
            f"PnL: {pnl:.2f}\n\n"
        )

    await update.message.reply_text(text)
    
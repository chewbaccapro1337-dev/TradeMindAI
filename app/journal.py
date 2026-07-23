from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import (
    save_trade,
    clear_trades,
    get_last_trades,
    get_open_trades,
    close_trade,
    get_statistics
)
from keyboards import (
    main_keyboard,
    back_keyboard,
    buy_sell_keyboard,
    symbol_keyboard,
    currency_keyboard,
)
from database import save_trade
from session import session_data
from states import (
    SYMBOL,
    SIDE,
    ENTRY,
    TP,
    SL,
    TRADE_RISK,
    POSITION_SIZE,
    COMMENT,
    SELECT_CLOSE_TRADE,
    CLOSE_PRICE,
    ACCOUNT_CURRENCY,
)

trade_data = session_data

BACK_TO_MENU = "menu"
BACK_TO_SYMBOL = "symbol"
BACK_TO_SIDE = "side"
BACK_TO_ENTRY = "entry"

async def ask_currency(update, context):

    await update.message.reply_text(
        "Выберите валюту счета:",
        reply_markup=currency_keyboard
    )

    return ACCOUNT_CURRENCY

async def get_currency(update, context):

    text = update.message.text

    if text == "💵 USD":
        context.user_data["currency"] = "USD"

    elif text == "₽ RUB":
        context.user_data["currency"] = "RUB"

    else:
        await update.message.reply_text(
            "Выберите валюту кнопкой"
        )
        return ACCOUNT_CURRENCY


    return await ask_symbol(update, context)

async def ask_symbol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in trade_data:
        trade_data[user_id] = {}

    trade_data[user_id]["module"] = "journal"
    trade_data[user_id]["back"] = BACK_TO_MENU

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
        trade_data[update.effective_user.id]["back"] = BACK_TO_ENTRY

        await update.message.reply_text(
            "🎯 Введите Take Profit (TP):",
            reply_markup=back_keyboard
        )

        return TP

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число.\nПример: 65000"
        )

        return ENTRY

async def get_tp(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "Отмена" in update.message.text:
        trade_data.pop(update.effective_user.id, None)

        await update.message.reply_text(
            "❌ Действие отменено.",
            reply_markup=main_keyboard
        )

        return ConversationHandler.END

    try:
        tp = float(update.message.text)

        trade_data[update.effective_user.id]["tp"] = tp

        await update.message.reply_text(
            "🛑 Введите Stop Loss (SL):",
            reply_markup=back_keyboard
        )

        return SL

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число."
        )

        return TP

async def get_sl(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "Отмена" in update.message.text:
        trade_data.pop(update.effective_user.id, None)

        await update.message.reply_text(
            "❌ Действие отменено.",
            reply_markup=main_keyboard
        )

        return ConversationHandler.END

    try:
        sl = float(update.message.text)

        trade_data[update.effective_user.id]["sl"] = sl

        currency = context.user_data.get("currency", "USD")
        await update.message.reply_text(
            f"💵 Введите риск сделки ({currency}):",
            reply_markup=back_keyboard
        )

        return TRADE_RISK

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число."
        )

        return SL

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

        return TRADE_RISK
async def get_trade_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        risk = float(update.message.text)

        user = trade_data[update.effective_user.id]

        user["risk"] = risk

        currency = context.user_data.get("currency", "USD")

        reward = (
            abs(user["tp"] - user["entry"])
            if user["side"] == "BUY"
            else abs(user["entry"] - user["tp"])
        )

        loss = (
            abs(user["entry"] - user["sl"])
            if user["side"] == "BUY"
            else abs(user["sl"] - user["entry"])
        )

        rr = reward / loss if loss != 0 else 0

        expected_profit = risk * rr

        save_trade(
            user_id=update.effective_user.id,
            symbol=user["symbol"],
            side=user["side"],
            entry=user["entry"],
            tp=user["tp"],
            sl=user["sl"],
            risk=risk,
            rr=rr,
            expected_profit=expected_profit,
            position_size=user.get("position_size"),
            comment=user.get("comment"),
            currency=currency
        )

        await update.message.reply_text(
            "✅ Сделка сохранена!\n\n"
            f"📈 {user['symbol']}\n"
            f"📊 {user['side']}\n"
            f"🎯 Потенциальная прибыль: {expected_profit:.2f} {currency}\n"
            f"📐 RR: 1:{rr:.2f}\n"
            f"⚠️ Риск: {risk:.2f} {currency}\n",
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

    print("SHOW LAST TRADES CALLED")

    trades = get_last_trades(
        update.effective_user.id,
        limit=20
    )

    if not trades:
        await update.message.reply_text(
            "📭 У вас пока нет сохранённых сделок."
        )
        return


    text = "📒 Последние 20 сделок:\n\n"


    for i, trade in enumerate(trades, start=1):

        symbol, side, entry, tp, sl, risk, rr, expected_profit, currency, status, created = trade

        rr = rr if rr is not None else 0
        expected_profit = expected_profit if expected_profit is not None else 0
        status = status if status is not None else "OPEN"

        status_icon = "🟢" if status == "OPEN" else "⚪"

        text += (
            f"{i}. {status_icon} {symbol} | {side}\n"
            f"📥 Вход: {entry}\n"
            f"🎯 TP: {tp}\n"
            f"🛑 SL: {sl}\n"
            f"⚠️ Риск: {risk:.2f} {currency}\n"
            f"📐 RR: 1:{rr:.2f}\n"
            f"💰 Потенциал: {expected_profit:.2f} {currency}\n"
            f"📌 Статус: {status}\n"
            f"📅 {created}\n"
            "━━━━━━━━━━━━━━\n\n"
        )


    await update.message.reply_text(text[:4000])

async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):

    stats = get_statistics(
        update.effective_user.id
    )


    if not stats[0]:
        await update.message.reply_text(
            "📊 Статистика пока пустая."
        )
        return


    (
        total,
        wins,
        losses,
        profit,
        loss,
        total_pnl,
        avg_win,
        avg_loss,
        best,
        worst

    ) = stats


    wins = wins or 0
    losses = losses or 0

    winrate = (
        wins / total * 100
        if total
        else 0
    )


    text = (
        "📊 Статистика трейдинга\n\n"

        f"Всего сделок: {total}\n"
        f"✅ Победы: {wins}\n"
        f"❌ Поражения: {losses}\n\n"

        f"🎯 Winrate: {winrate:.1f}%\n\n"

        f"💰 Прибыль: +{profit or 0:.2f}$\n"
        f"💸 Убыток: {loss or 0:.2f}$\n\n"

        f"📈 Итог: {total_pnl or 0:.2f}$\n\n"

        f"🔥 Лучшая сделка: {best or 0:.2f}$\n"
        f"💀 Худшая сделка: {worst or 0:.2f}$"
    )


    await update.message.reply_text(text)

async def start_close_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trades = get_open_trades(update.effective_user.id)

    if not trades:
        await update.message.reply_text(
            "📭 Нет открытых сделок."
        )
        return ConversationHandler.END

    text = "🔒 Выберите сделку для закрытия:\n\n"

    for i, trade in enumerate(trades, start=1):
        (
            trade_id,
            symbol,
            side,
            entry,
            tp,
            sl,
            risk,
            rr,
            expected_profit,
            created
        ) = trade

        text += (
            f"{i}. {symbol} {side}\n"
            f"📥 Вход: {entry}\n"
            f"🎯 TP: {tp}\n"
            f"🛑 SL: {sl}\n"
            f"⚠️ Риск: {risk}$\n\n"
        )

    context.user_data["close_trades"] = trades

    await update.message.reply_text(
        text,
        reply_markup=back_keyboard
    )

    return SELECT_CLOSE_TRADE

async def select_close_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("SELECT CLOSE TRADE CALLED")
    print("TEXT:", update.message.text)
    print("DATA:", context.user_data)

    try:
        index = int(update.message.text) - 1

        trades = context.user_data.get("close_trades")

        if not trades or index < 0 or index >= len(trades):
            await update.message.reply_text(
                "❌ Неверный номер сделки."
            )
            return SELECT_CLOSE_TRADE

        trade = trades[index]

        context.user_data["selected_trade"] = trade

        await update.message.reply_text(
            "💵 Введите цену выхода:",
            reply_markup=back_keyboard
        )

        return CLOSE_PRICE

    except ValueError:
        await update.message.reply_text(
            "❌ Введите номер сделки."
        )

        return SELECT_CLOSE_TRADE

async def close_trade_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        exit_price = float(update.message.text)

        trade = context.user_data["selected_trade"]

        (
            trade_id,
            symbol,
            side,
            entry,
            tp,
            sl,
            risk,
            rr,
            expected_profit,
            created
        ) = trade

        if side == "BUY":
            r_result = (exit_price - entry) / abs(entry - sl)
        else:
            r_result = (entry - exit_price) / abs(sl - entry)

        pnl = risk * r_result

        close_trade(
            trade_id,
            exit_price,
            pnl
        )

        await update.message.reply_text(
            "✅ Сделка закрыта!\n\n"
            f"📈 {symbol}\n"
            f"📊 {side}\n"
            f"📤 Выход: {exit_price}\n"
            f"💰 PnL: {pnl:.2f}$",
            reply_markup=main_keyboard
        )

        context.user_data.pop("selected_trade", None)
        context.user_data.pop("close_trades", None)

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Введите число."
        )

        return CLOSE_PRICE

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    clear_trades(update.effective_user.id)

    await update.message.reply_text(
        "🗑 История сделок очищена.\n"
        "📊 Статистика сброшена.",
        reply_markup=main_keyboard
    )

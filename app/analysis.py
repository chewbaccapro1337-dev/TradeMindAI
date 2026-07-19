from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards import back_keyboard, main_keyboard
import os
from ai import analyze_trade
from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels,
    detect_bos_choch,
    build_structure,
    label_structure,
    find_fvg,
    detect_liquidity_sweep,
    detect_market_structure,
    find_entry_zone,
)

ANALYZE = 20

async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Отправьте скриншот сделки.",
        reply_markup=back_keyboard
    )

    return ANALYZE

async def analyze_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Отправьте изображение."
        )
        return ANALYZE

    print("Фото получено")

    await update.message.reply_text("🔍 Анализирую сделку...")

    photo = update.message.photo[-1]
    file = await photo.get_file()

    os.makedirs("photos", exist_ok=True)

    file_path = f"photos/{update.effective_user.id}.jpg"

    await file.download_to_drive(file_path)

    await update.message.reply_text(
        "🤖 Анализирую график..."
    )

    result = analyze_trade(file_path)

    await update.message.reply_text(
        result,
        reply_markup=main_keyboard
    )

    return ConversationHandler.END

def analyze_market():

    candles = get_candles()

    highs, lows = find_swings(candles)

    structure = build_structure(
        highs,
        lows
    )

    labeled = label_structure(
        structure
    )


    market_structure = detect_market_structure(
        highs,
        lows
    )


    current_price = candles[-1]["close"]


    bos_choch = detect_bos_choch(
        labeled,
        current_price,
        market_structure["trend"]
    )


    fvgs = find_fvg(
        candles
    )


    equal_highs = find_equal_levels(
        highs
    )

    equal_lows = find_equal_levels(
        lows
    )


    sweep = detect_liquidity_sweep(
        candles,
        equal_lows,
        equal_highs
    )


    entry_zone = find_entry_zone(
        sweep,
        bos_choch,
        fvgs
    )


    signal = None

    if entry_zone:
        entry_text = (
            f"Зона интереса: "
            f"{entry_zone['low']} - {entry_zone['high']}"
        )
    else:
        entry_text = "Подходящая зона интереса не найдена"


    return {
        "trend": market_structure["trend"],
        "price": current_price,
        "bos_choch": bos_choch,
        "sweep": sweep,
        "entry_zone": entry_zone,
        "signal": signal
    }
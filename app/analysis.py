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
     "signal": signal,
     "fvgs": fvgs,
     "structure": labeled,
     "market_structure": market_structure
    }

def make_report():

    data = analyze_market()

    report = []

    # тренд
    report.append("📊 BTC MARKET ANALYSIS\n")

    if data["trend"] == "DOWN":
        report.append("Тренд: 🔴 DOWN")
    elif data["trend"] == "UP":
        report.append("Тренд: 🟢 UP")
    else:
        report.append("Тренд: ⚪ RANGE")


    # цена
    report.append(
        f"Цена: {data['price']}"
    )


    # структура

    bos = data["bos_choch"]

    if bos["event"]:
        report.append(
            f"Структура: {bos['event']} {bos['direction']}"
        )
    else:
        report.append(
            "Структура: ⏳ подтверждения нет"
        )


    # FVG

    fvgs = data.get("fvgs")

    if fvgs:

        fvg = fvgs[-1]

        report.append(
            f"""
📦 FVG:

Тип: {fvg['type']}
Зона: {fvg['low']} - {fvg['high']}
Размер: {round(fvg['size'], 2)}
"""
        )

    else:

        report.append(
            """
📦 FVG:
Не найден
"""
        )

    # ликвидность

    sweep = data["sweep"]

    if sweep:

        report.append(
            f"""
Ликвидность:
⚡ {sweep['type']}
Уровень: {sweep['level']}
Экстремум: {sweep['price']}
"""
        )

    else:

        report.append(
            "Ликвидность: не обнаружена"
        )


    # зона

    if data["entry_zone"]:

        zone = data["entry_zone"]

        report.append(
            f"""
Зона интереса:
{zone['low']} - {zone['high']}
"""
        )

    else:

        report.append(
            """
Зона интереса:
❌ не найдена
"""
        )


    return "\n".join(report)
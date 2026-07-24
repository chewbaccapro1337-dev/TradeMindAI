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
    detect_sweep_structure_break,
    find_buy_sell_liquidity,
    detect_pool_sweep,
    filter_fvg_by_confirmation,
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

    buy_side, sell_side = find_buy_sell_liquidity(candles)


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


    buy_side, sell_side = find_buy_sell_liquidity(
     candles
    )

    sweep = detect_pool_sweep(
     candles,
     buy_side,
     sell_side
    )
    
    sweep_structure = detect_sweep_structure_break(
     sweep,
     labeled,
     current_price
    )  

    entry_zone = None

    if sweep and sweep_structure:

       fvgs = find_fvg(candles)


       confirmed_fvgs = filter_fvg_by_confirmation(
         fvgs,
         sweep_structure
       )


       entry_zone = find_entry_zone(
          sweep,
          sweep_structure,
          confirmed_fvgs
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
     "fvgs": confirmed_fvgs,
     "structure": labeled,
     "market_structure": market_structure,
     "sweep_structure": sweep_structure,
     "buy_side": buy_side,
     "sell_side": sell_side
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

    buy = data.get("buy_side")
    sell = data.get("sell_side")


    report.append(
        "\n📍 Ликвидность:"
    )


    if buy:

        report.append(
            f"""
🟢 Buy Side
Цена: {buy['price']}
Сила: {buy['strength']}
"""
        )

    else:

        report.append(
            """
🟢 Buy Side
Не найдена
"""
        )


    if sell:

        report.append(
            f"""
🔴 Sell Side
Цена: {sell['price']}
Сила: {sell['strength']}
"""
        )

    else:

        report.append(
            """
🔴 Sell Side
Не найдена
"""
        )

    # Market Structure

    structure = data.get("structure")

    if structure:

        text = []

        for x in structure[-5:]:

            text.append(
                f"{x['label']}: {x['price']}"
            )

        report.append(
            "🏗 Структура рынка:\n" +
            "\n".join(text)
        )

    # ликвидность

        # Пулы ликвидности

    buy = data.get("buy_side")
    sell = data.get("sell_side")


    report.append(
        "\n📍 Liquidity Pools:\n"
    )


    if buy:

        report.append(
            f"""
🟢 Buy Side
Цена: {buy['price']:.2f}
Сила: {buy['strength']}
"""
        )

    else:

        report.append(
            """
🟢 Buy Side
Не найдена
"""
        )


    if sell:

        report.append(
            f"""
🔴 Sell Side
Цена: {sell['price']:.2f}
Сила: {sell['strength']}
"""
        )

    else:

        report.append(
            """
🔴 Sell Side
Не найдена
"""
        )


    # Sweep

    sweep = data.get("sweep")


    if sweep:

        report.append(
            f"""
⚡ Liquidity Sweep:

Тип:
{sweep['type']}

Уровень:
{sweep['level']}

Цена:
{sweep['price']}
"""
        )

    else:

        report.append(
            """
⚡ Liquidity Sweep:

Не обнаружен
"""
        )

    sweep_structure = data.get("sweep_structure")

    if sweep_structure:

        report.append(
            f"""
🏗 После Sweep:

{sweep_structure['event']}
Направление:
{sweep_structure['direction']}

Уровень:
{sweep_structure['level']}
"""
        )

    else:

        report.append(
            """
🏗 После Sweep:

Подтверждения структуры нет
"""
        )

    # Зона интереса

    if data.get("entry_zone"):

        zone = data["entry_zone"]

        report.append(
            f"""
🎯 Сетап найден

Зона интереса:

{zone['low']} - {zone['high']}
"""
        )

    else:

        report.append(
            """
🎯 Сетап:

⏳ ожидание подтверждения
"""
        )


    return "\n".join(report)
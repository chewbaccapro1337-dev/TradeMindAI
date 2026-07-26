import re


def parse_trade_voice(user_id, text):

    text = text.lower()


    symbol = "BTCUSDT"


    if "eur" in text or "евро" in text:
     symbol = "EURUSD"

    elif "gbp" in text or "фунт" in text:
     symbol = "GBPUSD"

    elif "jpy" in text or "йена" in text:
     symbol = "USDJPY"

    elif "eth" in text:
     symbol = "ETHUSDT"

    elif "sol" in text:
     symbol = "SOLUSDT"


    side = "BUY"


    short_words = [
     "шорт",
     "short",
     "sell",
     "селл",
     "продай",
     "продажа",
     "продавать",
     "медвеж"
    ]


    long_words = [
     "лонг",
     "long",
     "buy",
     "бай",
     "купи",
     "покупка"
    ]


    for word in short_words:
        if word in text:
            side = "SELL"
            break


    for word in long_words:
        if word in text:
            side = "BUY"
            break


    entry_match = re.search(
     r"вход\s*(\d+(?:\.\d+)?)",
     text
    )

    sl_match = re.search(
     r"стоп\s*(\d+(?:\.\d+)?)",
     text
    )

    tp_match = re.search(
     r"тейк\s*(\d+(?:\.\d+)?)",
     text
    )

    risk_match = re.search(
     r"риск\s*(\d+(?:\.\d+)?)",
     text
    )


    if not entry_match or not sl_match or not tp_match or not risk_match:
        return (
            "❌ Не смог разобрать сделку.\n\n"
            "Пример:\n"
            "Открой BTC лонг вход 65000 "
            "стоп 64000 тейк 67000 риск 50"
        )


    entry = float(entry_match.group(1))
    sl = float(sl_match.group(1))
    tp = float(tp_match.group(1))
    risk = float(risk_match.group(1))

    currency = "USD"

    print("VOICE TEXT:", text)

    if "руб" in text or "рублей" in text or "₽" in text:
     currency = "RUB"

    print("VOICE CURRENCY:", currency)

    # расчет RR
    rr = abs(tp - entry) / abs(entry - sl)


    # потенциальная прибыль
    expected_profit = risk * rr


    # пока размер позиции считаем автоматически позже
    position_size = 0


    # комментарий для журнала
    comment = "Создано голосовым помощником"


    from database import save_trade


    save_trade(
        user_id=user_id,
        symbol=symbol,
        side=side,
        entry=entry,
        tp=tp,
        sl=sl,
        risk=risk,
        rr=rr,
        expected_profit=expected_profit,
        position_size=position_size,
        comment=comment,
        currency=currency
    )

    currency_symbol = "$"

    if currency == "RUB":
     currency_symbol = "₽"

    return (
     f"✅ Сделка добавлена\n\n"
     f"{symbol} {side}\n\n"
     f"📥 Вход: {entry}\n"
     f"🎯 TP: {tp}\n"
     f"🛑 SL: {sl}\n"
     f"⚠️ Риск: {risk}{currency_symbol}\n"
     f"📐 RR: 1:{rr:.2f}\n"
     f"💰 Потенциал: {risk*rr:.2f}{currency_symbol}"
    )
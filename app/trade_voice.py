import re


def parse_trade_voice(user_id, text):

    text = text.lower()


    symbol = "BTCUSDT"

    if "eth" in text:
        symbol = "ETHUSDT"


    side = "BUY"

    if "шорт" in text or "sell" in text:
        side = "SELL"



    entry = re.search(
        r"вход\s*(\d+)",
        text
    )

    sl = re.search(
        r"стоп\s*(\d+)",
        text
    )

    tp = re.search(
        r"тейк\s*(\d+)",
        text
    )

    risk = re.search(
        r"риск\s*(\d+)",
        text
    )


    if not entry or not sl or not tp or not risk:
        return (
            "❌ Не смог разобрать сделку.\n\n"
            "Пример:\n"
            "Открой BTC лонг вход 65000 "
            "стоп 64000 тейк 67000 риск 50"
        )


    entry = float(entry.group(1))
    sl = float(sl.group(1))
    tp = float(tp.group(1))
    risk = float(risk.group(1))


    rr = abs(tp-entry) / abs(entry-sl)


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
        expected_profit=risk*rr,
        currency="USD"
    )


    return (
        f"✅ Сделка добавлена\n\n"
        f"{symbol} {side}\n\n"
        f"📥 Вход: {entry}\n"
        f"🎯 TP: {tp}\n"
        f"🛑 SL: {sl}\n"
        f"⚠️ Риск: {risk}$\n"
        f"📐 RR: 1:{rr:.2f}"
    )
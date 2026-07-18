from market_analyzer import analyze_market


def make_report():

    data = analyze_market()

    price = data["price"]
    buy = data["buy_side"]
    sell = data["sell_side"]

    buy_distance = buy["price"] - price
    sell_distance = price - sell["price"]

    if buy_distance < sell_distance:
        direction = "🟢 BUY SIDE"
        probability = 65 + min(30, buy["strength"] // 5)
        target = buy
    else:
        direction = "🔴 SELL SIDE"
        probability = 65 + min(30, sell["strength"] // 5)
        target = sell

    text = (
        "🧠 TRADEMIND AI\n"
        "══════════════════════\n\n"

        f"💰 Цена BTC: {price:.2f}\n\n"

        "📍 Ближайшая ликвидность\n\n"

        f"🟢 Buy Side\n"
        f"Цена: {buy['price']:.2f}\n"
        f"Сила: {buy['strength']}\n\n"

        f"🔴 Sell Side\n"
        f"Цена: {sell['price']:.2f}\n"
        f"Сила: {sell['strength']}\n\n"

        "══════════════════════\n\n"

        f"🎯 Вероятная цель:\n{direction}\n\n"

        f"📊 Вероятность: {probability}%\n\n"

        f"🎯 Следующий магнит цены:\n{target['price']:.2f}"
    )

    return text

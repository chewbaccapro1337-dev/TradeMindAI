from market_analyzer import analyze_market


def make_report():

    data = analyze_market()

    price = data["price"]

    buy = data.get("buy_side")
    sell = data.get("sell_side")


    text = (
        "🧠 TRADEMIND AI\n"
        "══════════════════════\n\n"
        f"💰 Цена BTC: {price:.2f}\n\n"
        "📍 Ближайшая ликвидность\n\n"
    )


    buy_distance = None
    sell_distance = None


    if buy:

        buy_distance = buy["price"] - price

        text += (
            "🟢 Buy Side\n"
            f"Цена: {buy['price']:.2f}\n"
            f"Сила: {buy['strength']}\n\n"
        )

    else:

        text += (
            "🟢 Buy Side\n"
            "Не найдена\n\n"
        )


    if sell:

        sell_distance = price - sell["price"]

        text += (
            "🔴 Sell Side\n"
            f"Цена: {sell['price']:.2f}\n"
            f"Сила: {sell['strength']}\n\n"
        )

    else:

        text += (
            "🔴 Sell Side\n"
            "Не найдена\n\n"
        )


    text += "══════════════════════\n\n"


    if buy and sell:

        if buy_distance < sell_distance:

            direction = "🟢 BUY SIDE"
            probability = 65 + min(30, buy["strength"] // 5)
            target = buy

        else:

            direction = "🔴 SELL SIDE"
            probability = 65 + min(30, sell["strength"] // 5)
            target = sell


        text += (
            f"🎯 Вероятная цель:\n"
            f"{direction}\n\n"
            f"📊 Вероятность: {probability}%\n\n"
            f"🎯 Следующий магнит цены:\n"
            f"{target['price']:.2f}"
        )

    elif buy:

        text += (
            "🎯 Найдена только BUY ликвидность\n\n"
            f"Цена магнита:\n{buy['price']:.2f}"
        )

    elif sell:

        text += (
            "🎯 Найдена только SELL ликвидность\n\n"
            f"Цена магнита:\n{sell['price']:.2f}"
        )

    else:

        text += (
            "⚠️ Ликвидность не найдена"
        )


    return text

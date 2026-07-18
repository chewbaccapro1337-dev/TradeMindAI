from market_data import get_candles
from liquidity import find_liquidity_zones


def analyze_market():
    candles = get_candles()

    current_price = candles[-1]["close"]

    zones = find_liquidity_zones(candles)

    buy_side = None
    sell_side = None

    for zone in zones:
        mid = (zone["low"] + zone["high"]) / 2

        if mid > current_price:
            if buy_side is None or mid < buy_side["price"]:
                buy_side = {
                    "price": mid,
                    "strength": zone["strength"]
                }

        else:
            if sell_side is None or mid > sell_side["price"]:
                sell_side = {
                    "price": mid,
                    "strength": zone["strength"]
                }

    return {
        "price": current_price,
        "buy_side": buy_side,
        "sell_side": sell_side
    }

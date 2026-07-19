import requests


def get_candles(symbol="BTCUSDT", interval="15m", limit=100):

    url = "https://fapi.binance.com/fapi/v1/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    candles = []

    for c in data:
        candles.append({
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4])
        })

    return candles

def find_swings(candles, left=2, right=2):

    swing_highs = []
    swing_lows = []

    for i in range(left, len(candles) - right):

        high = candles[i]["high"]
        low = candles[i]["low"]

        is_high = True
        is_low = True

        # Проверяем соседние свечи слева
        for j in range(1, left + 1):

            if candles[i - j]["high"] >= high:
                is_high = False

            if candles[i - j]["low"] <= low:
                is_low = False

        # Проверяем соседние свечи справа
        for j in range(1, right + 1):

            if candles[i + j]["high"] > high:
                is_high = False

            if candles[i + j]["low"] < low:
                is_low = False

        if is_high:
            swing_highs.append({
                "index": i,
                "price": high
            })

        if is_low:
            swing_lows.append({
                "index": i,
                "price": low
            })

    return swing_highs, swing_lows

def find_equal_levels(levels, tolerance=5):

    levels = sorted(levels, key=lambda x: x["price"])

    groups = []
    current = [levels[0]]

    for level in levels[1:]:

        if abs(level["price"] - current[-1]["price"]) <= tolerance:
            current.append(level)

        else:
            if len(current) >= 2:
                groups.append(current)

            current = [level]

    if len(current) >= 2:
        groups.append(current)

    result = []

    for group in groups:

        result.append({
            "price": sum(x["price"] for x in group) / len(group),
            "strength": len(group)
        })

    return result

def detect_bos(highs, lows, current_price):

    bos = None

    if highs:
        last_high = highs[-1]["price"]

        if current_price > last_high:
            bos = "BOS_UP"

    if lows:
        last_low = lows[-1]["price"]

        if current_price < last_low:
            bos = "BOS_DOWN"

    return bos

def find_liquidity_zones(candles, distance=50):

    prices = []

    for candle in candles:
        prices.append(candle["high"])
        prices.append(candle["low"])

    prices.sort()

    zones = []

    current_zone = [prices[0]]

    for price in prices[1:]:

        if price - current_zone[-1] <= distance:
            current_zone.append(price)
        else:
            zones.append(current_zone)
            current_zone = [price]

    zones.append(current_zone)

    result = []

    for zone in zones:
        result.append({
            "low": min(zone),
            "high": max(zone),
            "strength": len(zone)
        })

    return result

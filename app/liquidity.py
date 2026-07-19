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

def find_swings(candles):

    swing_highs = []
    swing_lows = []

    for i in range(2, len(candles) - 2):

        high = candles[i]["high"]

        if (
            high > candles[i-1]["high"]
            and high > candles[i-2]["high"]
            and high > candles[i+1]["high"]
            and high > candles[i+2]["high"]
        ):
            swing_highs.append(high)

        low = candles[i]["low"]

        if (
            low < candles[i-1]["low"]
            and low < candles[i-2]["low"]
            and low < candles[i+1]["low"]
            and low < candles[i+2]["low"]
        ):
            swing_lows.append(low)

    return swing_highs, swing_lows

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

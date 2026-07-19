from liquidity import (
    get_candles,
    find_swings,
    detect_bos
)

candles = get_candles()

highs, lows = find_swings(candles)

price = candles[-1]["close"]

bos = detect_bos(
    highs,
    lows,
    price
)

print(price)
print(bos)
from liquidity import (
    get_candles,
    find_swings,
    detect_bos
)

candles = get_candles()

highs, lows = find_swings(candles)

price = candles[-1]["close"]

print(type(highs[-1]))
print(highs[-1])

print(type(lows[-1]))
print(lows[-1])

bos = detect_bos(
    highs,
    lows,
    price
)

print(price)
print(bos)
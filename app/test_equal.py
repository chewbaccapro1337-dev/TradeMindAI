from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels,
    detect_bos
)

candles = get_candles()

highs, lows = find_swings(candles)

print("SWING HIGHS:")
print(highs[:3])

print()

print("SWING LOWS:")
print(lows[:3])

print()

eqh = find_equal_levels(highs)
eql = find_equal_levels(lows)

print("EQUAL HIGHS")
print(eqh)

print()

print("EQUAL LOWS")
print(eql)

print()

price = candles[-1]["close"]

bos = detect_bos(
    highs,
    lows,
    price
)

print("CURRENT PRICE:", price)
print("BOS:", bos)
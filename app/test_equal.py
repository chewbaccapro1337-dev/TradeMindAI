from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels
)

candles = get_candles()

highs, lows = find_swings(candles)

eqh = find_equal_levels(highs)
eql = find_equal_levels(lows)

print("EQUAL HIGHS")
print(eqh)

print()

print("EQUAL LOWS")
print(eql)
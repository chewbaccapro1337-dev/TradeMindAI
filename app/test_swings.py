from liquidity import get_candles, find_swings

candles = get_candles()

highs, lows = find_swings(candles)

print("HIGHS")
print(highs)

print()

print("LOWS")
print(lows)
from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels,
    detect_bos_choch,
    build_structure,
    label_structure,
    find_fvg,
    detect_liquidity_sweep
)


# =====================
# CANDLES
# =====================

candles = get_candles()


# =====================
# SWINGS
# =====================

highs, lows = find_swings(candles)


# =====================
# STRUCTURE
# =====================

structure = build_structure(
    highs,
    lows
)


labeled = label_structure(
    structure
)

print("\nLAST STRUCTURE:")
print(labeled[-5:])
print("\nLABELED STRUCTURE")

current_price = candles[-1]["close"]
print("\nLAST PRICE:")
print(current_price)


for s in labeled:
    print(s)



market_structure = detect_market_structure(
    highs,
    lows
)

# =====================
# PRICE
# =====================

current_price = candles[-1]["close"]


# берем последний известный тренд

trend = labeled[-1]["trend"]


print("\nCURRENT TREND")
print(trend)



# =====================
# BOS / CHoCH
# =====================

bos_choch = detect_bos_choch(
    labeled,
    current_price,
    market_structure["trend"]
)


print("\nBOS / CHoCH")
print(bos_choch)



# =====================
# FVG
# =====================

fvgs = find_fvg(
    candles
)


print("\nFVG")

for fvg in fvgs:
    print(fvg)



# =====================
# LIQUIDITY
# =====================

equal_highs = find_equal_levels(
    highs
)

equal_lows = find_equal_levels(
    lows
)


print("\nEQUAL HIGHS")

for x in equal_highs:
    print(x)


print("\nEQUAL LOWS")

for x in equal_lows:
    print(x)



sweep = detect_liquidity_sweep(
    candles,
    equal_lows,
    equal_highs
)


print("\nLIQUIDITY SWEEP")
print(sweep)



print("\nPRICE")
print(current_price)


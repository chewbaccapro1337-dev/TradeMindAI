from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels,
    detect_bos_choch,
    build_structure,
    label_structure,
    find_fvg,
    filter_fvg_by_trend,
    get_best_fvg,
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


print("\nLABELED STRUCTURE")

for s in labeled:
    print(s)



# =====================
# CURRENT PRICE
# =====================

current_price = candles[-1]["close"]



# =====================
# BOS / CHoCH
# =====================

bos_choch = detect_bos_choch(
    labeled,
    current_price
)


print("\nBOS / CHoCH")
print(bos_choch)



# =====================
# FVG
# =====================

fvgs = find_fvg(
    candles
)


print("\nALL FVG")

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



# =====================
# SWEEP
# =====================

sweep = detect_liquidity_sweep(
    candles,
    equal_lows,
    equal_highs
)


print("\nLIQUIDITY SWEEP")
print(sweep)



# =====================
# END
# =====================

print("\nPRICE:")
print(current_price)
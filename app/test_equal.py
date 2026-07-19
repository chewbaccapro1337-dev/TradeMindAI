from liquidity import (
    get_candles,
    find_swings,
    find_equal_levels,
    detect_bos,
    detect_market_structure,
    build_structure,
    label_structure,
    detect_choch,
    find_fvg,
    filter_fvg_by_trend
)

candles = get_candles()

# получаем swing точки
highs, lows = find_swings(candles)

# строим общую структуру
structure = build_structure(
    highs,
    lows
)

labeled = label_structure(
    structure
)

choch = detect_choch(
    labeled
)

fvgs = find_fvg(candles)

filtered_fvg = filter_fvg_by_trend(
    fvgs,
    label_structure
)


print("\nTREND FVG:")

for fvg in filtered_fvg:
    print(fvg)

print("\nFVG:")

for fvg in fvgs:
    print(fvg)


print()
print("CHoCH:")
print(choch)

print()
print("LABELED STRUCTURE")


for s in labeled:
    print(s)

print("STRUCTURE")

for s in structure:
    print(s)

candles = get_candles()

structure = build_structure(
    highs,
    lows
)

print()

print("STRUCTURE")

for s in structure[:20]:
    print(s)


structure = detect_market_structure(
    highs,
    lows
)

print()
print("MARKET STRUCTURE")
print(structure)

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
if bos:
    print(bos["type"])
    print(bos["level"])
else:
    print("NO BOS")
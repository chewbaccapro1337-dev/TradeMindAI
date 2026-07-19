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
    filter_fvg_by_trend,
    get_best_fvg,
    detect_liquidity_sweep
)

candles = get_candles()

## получаем swing точки
highs, lows = find_swings(candles)


# строим структуру
structure = build_structure(
    highs,
    lows
)


# ставим HH HL LH LL
labeled = label_structure(
    structure
)


# определяем тренд
market_structure = detect_market_structure(
    highs,
    lows
)


# CHoCH
choch = detect_choch(
    labeled
)


# FVG
fvgs = find_fvg(
    candles
)

print("MARKET:")
print(market_structure)

# фильтр по тренду
filtered_fvg = filter_fvg_by_trend(
    fvgs,
    market_structure
)

current_price = candles[-1]["close"]


best_fvg = get_best_fvg(
    filtered_fvg,
    current_price
)


print("\nBEST FVG:")
print(best_fvg)


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

equal_highs = find_equal_levels(highs)
equal_lows = find_equal_levels(lows)

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


print("\nLIQUIDITY SWEEP:")
print(sweep)

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
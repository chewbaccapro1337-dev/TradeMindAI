from app.liquidity import find_liquidity_zones


prices = [
64082,
64098,
64122,
64148,
64179,
63945,
63966,
63985,
63997
]


zones = find_liquidity_zones(prices)


for z in zones:
    print(z)


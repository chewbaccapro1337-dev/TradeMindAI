import requests


def get_candles(symbol="BTCUSDT", interval="15m", limit=100):

    url = "https://fapi.binance.com/fapi/v1/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    candles = []

    for c in data:
        candles.append({
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4])
        })

    return candles

def find_swings(candles, left=2, right=2):

    swing_highs = []
    swing_lows = []

    for i in range(left, len(candles) - right):

        high = candles[i]["high"]
        low = candles[i]["low"]

        is_high = True
        is_low = True

        # Проверяем соседние свечи слева
        for j in range(1, left + 1):

            if candles[i - j]["high"] >= high:
                is_high = False

            if candles[i - j]["low"] <= low:
                is_low = False

        # Проверяем соседние свечи справа
        for j in range(1, right + 1):

            if candles[i + j]["high"] > high:
                is_high = False

            if candles[i + j]["low"] < low:
                is_low = False

        if is_high:
            swing_highs.append({
                "index": i,
                "price": high
            })

        if is_low:
            swing_lows.append({
                "index": i,
                "price": low
            })

    return swing_highs, swing_lows

def build_structure(highs, lows):

    swings = []

    for high in highs:
        swings.append({
            "index": high["index"],
            "price": high["price"],
            "kind": "HIGH"
        })

    for low in lows:
        swings.append({
            "index": low["index"],
            "price": low["price"],
            "kind": "LOW"
        })


    swings.sort(
        key=lambda x: x["index"]
    )


    clean = []

    for swing in swings:

        if len(clean) == 0:
            clean.append(swing)
            continue


        last = clean[-1]


        # если два одинаковых типа подряд
        if last["kind"] == swing["kind"]:

            # оставляем более сильный экстремум
            if swing["kind"] == "HIGH":

                if swing["price"] > last["price"]:
                    clean[-1] = swing

            else:

                if swing["price"] < last["price"]:
                    clean[-1] = swing

        else:

            clean.append(swing)


    return clean

def label_structure(swings):

    labeled = []

    trend = None

    last_high = None
    last_low = None


    for swing in swings:

        item = swing.copy()


        if swing["kind"] == "HIGH":

            if last_high is None:
                item["label"] = "HIGH"

            else:

                if swing["price"] > last_high:

                    item["label"] = "HH"

                    trend = "UP"

                else:

                    item["label"] = "LH"

                    if trend == "UP":
                        trend = "DOWN"


            last_high = swing["price"]



        elif swing["kind"] == "LOW":

            if last_low is None:

                item["label"] = "LOW"


            else:

                if swing["price"] > last_low:

                    item["label"] = "HL"

                else:

                    item["label"] = "LL"

                    if trend == "DOWN":
                        trend = "DOWN"


            last_low = swing["price"]


        item["trend"] = trend

        labeled.append(item)


    return labeled

def detect_choch(labeled):

    if len(labeled) < 4:
        return None


    last = labeled[-1]
    previous = labeled[-2]


    recent = [
        x["label"]
        for x in labeled[-6:]
    ]


    # смена вверх -> вниз
    if (
        "HH" in recent
        and "HL" in recent
        and last["label"] == "LL"
    ):
        return {
            "type": "CHoCH_DOWN",
            "price": last["price"]
        }


    # смена вниз -> вверх
    if (
        "LH" in recent
        and "LL" in recent
        and last["label"] == "HH"
    ):
        return {
            "type": "CHoCH_UP",
            "price": last["price"]
        }


    return None

def find_fvg(candles, min_size=20):

    fvgs = []

    for i in range(2, len(candles)):

        candle1 = candles[i-2]
        candle3 = candles[i]


        # bullish imbalance

        if candle1["high"] < candle3["low"]:

            gap = candle3["low"] - candle1["high"]

            if gap >= min_size:

                fvgs.append({
                    "type": "BULLISH",
                    "low": candle1["high"],
                    "high": candle3["low"],
                    "size": gap,
                    "index": i
                })


        # bearish imbalance

        if candle1["low"] > candle3["high"]:

            gap = candle1["low"] - candle3["high"]

            if gap >= min_size:

                fvgs.append({
                    "type": "BEARISH",
                    "low": candle3["high"],
                    "high": candle1["low"],
                    "size": gap,
                    "index": i
                })


    return fvgs

def filter_fvg_by_trend(fvgs, structure):

    trend = structure["trend"]

    result = []

    for fvg in fvgs:

        if trend == "UP" and fvg["type"] == "BULLISH":
            result.append(fvg)


        elif trend == "DOWN" and fvg["type"] == "BEARISH":
            result.append(fvg)


    return result

def get_best_fvg(fvgs, current_price):

    valid = []

    for fvg in fvgs:

        # только зоны ниже цены при восходящем тренде
        if fvg["high"] < current_price:
            valid.append(fvg)


    if not valid:
        return None


    # выбираем ближайшую к цене
    best = max(
        valid,
        key=lambda x: x["high"]
    )


    return best

def find_equal_levels(levels, tolerance=5):

    levels = sorted(levels, key=lambda x: x["price"])

    groups = []
    current = [levels[0]]

    for level in levels[1:]:

        if abs(level["price"] - current[-1]["price"]) <= tolerance:
            current.append(level)

        else:
            if len(current) >= 2:
                groups.append(current)

            current = [level]

    if len(current) >= 2:
        groups.append(current)

    result = []

    for group in groups:

        result.append({
            "price": sum(x["price"] for x in group) / len(group),
            "strength": len(group)
        })

    return result

def detect_bos_choch(labeled, current_price):

    result = {
        "bos": None,
        "choch": None,
        "level": None
    }


    highs = [
        x for x in labeled
        if x["kind"] == "HIGH"
    ]

    lows = [
        x for x in labeled
        if x["kind"] == "LOW"
    ]


    if len(highs) < 2 or len(lows) < 2:
        return result



    # ==========================
    # BULLISH STRUCTURE
    # ==========================


    hh = [
        x for x in highs
        if x["label"] == "HH"
    ]

    hl = [
        x for x in lows
        if x["label"] == "HL"
    ]


    if hh and hl:

        last_hh = hh[-1]
        last_hl = hl[-1]


        # пробой последнего HH

        if current_price > last_hh["price"]:

            return {
                "bos": "BULLISH",
                "choch": None,
                "level": last_hh["price"]
            }



        # слом HL

        if current_price < last_hl["price"]:

            return {
                "bos": None,
                "choch": "BEARISH",
                "level": last_hl["price"]
            }



    # ==========================
    # BEARISH STRUCTURE
    # ==========================


    ll = [
        x for x in lows
        if x["label"] == "LL"
    ]


    lh = [
        x for x in highs
        if x["label"] == "LH"
    ]


    if ll and lh:

        last_ll = ll[-1]
        last_lh = lh[-1]


        if current_price < last_ll["price"]:

            return {
                "bos": "BEARISH",
                "choch": None,
                "level": last_ll["price"]
            }



        if current_price > last_lh["price"]:

            return {
                "bos": None,
                "choch": "BULLISH",
                "level": last_lh["price"]
            }


    return result

def find_liquidity_zones(candles, distance=50):

    prices = []

    for candle in candles:
        prices.append(candle["high"])
        prices.append(candle["low"])

    prices.sort()

    zones = []

    current_zone = [prices[0]]

    for price in prices[1:]:

        if price - current_zone[-1] <= distance:
            current_zone.append(price)
        else:
            zones.append(current_zone)
            current_zone = [price]

    zones.append(current_zone)

    result = []

    for zone in zones:
        result.append({
            "low": min(zone),
            "high": max(zone),
            "strength": len(zone)
        })

    return result

def detect_market_structure(highs, lows):

    if len(highs) < 2 or len(lows) < 2:
        return None


    last_high = highs[-1]["price"]
    prev_high = highs[-2]["price"]

    last_low = lows[-1]["price"]
    prev_low = lows[-2]["price"]


    structure = {
        "trend": None,
        "last_high": last_high,
        "last_low": last_low,
        "prev_high": prev_high,
        "prev_low": prev_low,
        "event": None
    }


    # пробой прошлого хая = бычий перелом/продолжение

    if last_high > prev_high:

        structure["trend"] = "UP"

        structure["event"] = {
            "type": "CHoCH_UP",
            "price": last_high
        }


    # пробой прошлого лоя = медвежий перелом

    elif last_low < prev_low:

        structure["trend"] = "DOWN"

        structure["event"] = {
            "type": "CHoCH_DOWN",
            "price": last_low
        }


    else:

        structure["trend"] = "RANGE"


    return structure

def detect_liquidity_sweep(
    candles,
    equal_lows,
    equal_highs
):

    current_price = candles[-1]["close"]

    sweep = None


    # поиск снятия равных минимумов

    for low in equal_lows:

        level = low["price"]

        if current_price > level:

            recent_low = min(
                c["low"] for c in candles[-10:]
            )


            if recent_low < level:

                sweep = {
                    "type": "LOW_SWEEP",
                    "level": level,
                    "price": recent_low
                }


    # поиск снятия равных максимумов

    for high in equal_highs:

        level = high["price"]

        if current_price < level:

            recent_high = max(
                c["high"] for c in candles[-10:]
            )


            if recent_high > level:

                sweep = {
                    "type": "HIGH_SWEEP",
                    "level": level,
                    "price": recent_high
                }


    return sweep

def detect_sweep_structure_break(
    sweep,
    labeled,
    current_price
):

    if sweep is None:
        return None


    last_hl = None
    last_lh = None


    # ищем последние защищенные уровни
    for x in labeled:

        if x["label"] == "HL":
            last_hl = x

        elif x["label"] == "LH":
            last_lh = x



    result = {
        "event": None,
        "direction": None,
        "level": None
    }


    # =========================
    # HIGH SWEEP
    # =========================

    if sweep["type"] == "HIGH_SWEEP":


        # после снятия хай ликвидности
        # ждем пробой HL вниз

        if last_hl:

            if current_price < last_hl["price"]:

                result["event"] = "CHoCH"
                result["direction"] = "BEARISH"
                result["level"] = last_hl["price"]

                return result



        # если цена вернулась вверх и обновила хай

        if current_price > sweep["price"]:

            result["event"] = "BOS"
            result["direction"] = "BULLISH"
            result["level"] = sweep["price"]

            return result



    # =========================
    # LOW SWEEP
    # =========================

    if sweep["type"] == "LOW_SWEEP":


        # пробой LH вверх

        if last_lh:

            if current_price > last_lh["price"]:

                result["event"] = "CHoCH"
                result["direction"] = "BULLISH"
                result["level"] = last_lh["price"]

                return result



        # обновление минимума

        if current_price < sweep["price"]:

            result["event"] = "BOS"
            result["direction"] = "BEARISH"
            result["level"] = sweep["price"]

            return result



    return result
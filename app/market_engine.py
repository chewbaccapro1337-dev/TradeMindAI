from analysis import analyze_market
from news import build_news_text


def build_market_context():

    context = {}

    print("📊 Loading BTC...")
    context["btc"] = analyze_market("BTCUSDT")


    print("💵 Loading DXY...")
    context["dxy"] = analyze_market("DXY")


    print("🥇 Loading GOLD...")
    context["gold"] = analyze_market("XAUUSD")


    print("📈 Loading SP500...")
    context["sp500"] = analyze_market("SPX")


    print("₿ Loading BTC Dominance...")
    context["btc_dominance"] = analyze_market("BTC.D")


    print("📰 Loading News...")
    context["news"] = build_news_text()


    return context
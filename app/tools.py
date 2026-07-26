def btc_analysis_tool(user_id):

    from analysis import make_report

    return make_report()



def statistics_tool(user_id):

    from journal import build_statistics_text

    return build_statistics_text(
        user_id
    )



def last_trades_tool(user_id):

    from journal import build_last_trades_text

    return build_last_trades_text(
        user_id
    )

def news_tool(user_id, symbol=None):

    from news import build_news_text

   return build_news_text(symbol)

def market_brief_tool(user_id):

    from analysis import make_report
    from news import build_news_text


    btc = make_report()

    news = build_news_text()


    return f"""
📊 TradeMind Market Brief

{news}


━━━━━━━━━━━━━━


₿ BTC Анализ:

{btc}
"""
import yfinance as yf


def get_price(ticker):

    try:

        data = yf.Ticker(ticker)

        price = data.history(
            period="1d",
            interval="5m"
        )

        if price.empty:
            return None

        last = price["Close"].iloc[-1]

        return round(float(last), 2)


    except Exception as e:

        print("MARKET DATA ERROR:", ticker, e)

        return None



def get_market_context():

    return {

        "DXY": {
            "price": get_price("DX-Y.NYB")
        },


        "GOLD": {
            "price": get_price("GC=F")
        },


        "SP500": {
            "price": get_price("^GSPC")
        }

    }
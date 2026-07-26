import yfinance as yf


def get_price(ticker):

    try:

        data = yf.download(
            ticker,
            period="5d",
            interval="15m",
            progress=False,
            auto_adjust=False
        )


        if data.empty:
            print("EMPTY:", ticker)
            return None


        price = data["Close"].iloc[-1]


        if hasattr(price, "iloc"):
            price = price.iloc[0]


        return round(float(price), 2)


    except Exception as e:

        print(
            "MARKET ERROR:",
            ticker,
            e
        )

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
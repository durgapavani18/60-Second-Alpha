import yfinance as yf

def get_stock_data(ticker="RELIANCE.NS"):
    """
    Fetch stock data for the given NSE ticker.
    Pass ticker dynamically from the user's input.
    Example tickers: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")

        if hist.empty:
            return {
                "ticker": ticker,
                "price": None,
                "sma_20": None,
                "signal": "No Data",
                "rsi": None,
                "volume": None,
                "error": f"No data found for ticker: {ticker}"
            }

        latest_price = hist['Close'].iloc[-1]
        sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
        avg_volume = hist['Volume'].mean()
        latest_volume = hist['Volume'].iloc[-1]

        # RSI calculation (14-period)
        delta = hist['Close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]

        # Signal logic
        if latest_price > sma_20 and rsi < 70:
            signal = "Bullish"
        elif latest_price < sma_20 and rsi > 30:
            signal = "Bearish"
        elif rsi >= 70:
            signal = "Overbought"
        elif rsi <= 30:
            signal = "Oversold"
        else:
            signal = "Neutral"

        # Get company info
        info = stock.info
        company_name = info.get("longName", ticker.replace(".NS", ""))

        return {
            "ticker": ticker,
            "company_name": company_name,
            "price": round(float(latest_price), 2),
            "sma_20": round(float(sma_20), 2),
            "rsi": round(float(rsi), 1),
            "volume": int(latest_volume),
            "avg_volume": int(avg_volume),
            "signal": signal,
            "error": None
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "price": None,
            "sma_20": None,
            "signal": "Error",
            "rsi": None,
            "volume": None,
            "error": str(e)
        }
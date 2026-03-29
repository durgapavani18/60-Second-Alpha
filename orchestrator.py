from stock_agent import get_stock_data
from news_agent import get_news_sentiment


def generate_insight(ticker: str = "RELIANCE.NS") -> dict:
    """
    Orchestrate stock data + news sentiment into a structured insight dict.
    Returns both the formatted text and raw data for downstream use.
    """
    print(f"[Orchestrator] Fetching data for {ticker}...")

    stock = get_stock_data(ticker)
    news = get_news_sentiment(
        company_name=stock.get("company_name", ""),
        ticker=ticker
    )

    if stock.get("error"):
        return {
            "success": False,
            "error": stock["error"],
            "stock": stock,
            "news": news,
            "text": f"Could not fetch data for {ticker}. Please check the ticker symbol."
        }

    # Volume analysis
    vol_ratio = stock["volume"] / stock["avg_volume"] if stock["avg_volume"] else 1
    volume_note = "above average" if vol_ratio > 1.2 else "below average" if vol_ratio < 0.8 else "normal"

    # Compose the insight text (this is what the LLM will refine in script_generator)
    insight_text = f"""
Stock: {stock['company_name']} ({stock['ticker']})
Current Price: ₹{stock['price']}
20-Day SMA: ₹{stock['sma_20']}
RSI (14): {stock['rsi']}
Volume: {volume_note} ({stock['volume']:,} vs avg {stock['avg_volume']:,})
Signal: {stock['signal']}

News Sentiment: {news['sentiment']} (score: {news['score']})
Top Headlines:
{chr(10).join(f"- {h}" for h in news['headlines'][:3])}
""".strip()

    return {
        "success": True,
        "error": None,
        "stock": stock,
        "news": news,
        "text": insight_text
    }
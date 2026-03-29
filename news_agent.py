import os
import requests
import xml.etree.ElementTree as ET
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")  # Set this in your environment


def fetch_newsapi_headlines(company_name: str, ticker: str) -> list[str]:
    """Fetch headlines from NewsAPI (free tier: 100 calls/day)."""
    if not NEWS_API_KEY:
        return []

    # Use company name without .NS suffix for better results
    clean_name = company_name or ticker.replace(".NS", "")
    query = f"{clean_name} stock NSE India"

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": NEWS_API_KEY
        }
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])
            return [a["title"] for a in articles if a.get("title")]
    except Exception as e:
        print(f"[NewsAPI error] {e}")

    return []


def fetch_et_rss_headlines() -> list[str]:
    """Fallback: fetch latest headlines from ET Markets RSS feed."""
    rss_urls = [
        "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    ]

    headlines = []
    for url in rss_urls:
        try:
            response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            for item in items[:8]:
                title = item.find("title")
                if title is not None and title.text:
                    headlines.append(title.text.strip())
        except Exception as e:
            print(f"[ET RSS error] {e}")

    return headlines[:10]


def get_news_sentiment(company_name: str = "", ticker: str = "RELIANCE.NS") -> dict:
    """
    Fetch live news headlines for the given stock/company and run sentiment analysis.
    Falls back to ET Markets RSS if NewsAPI key is not set.
    """
    headlines = fetch_newsapi_headlines(company_name, ticker)

    if not headlines:
        print("[News] Falling back to ET Markets RSS feed...")
        headlines = fetch_et_rss_headlines()

    if not headlines:
        # Last resort: use generic neutral placeholders
        headlines = [
            f"{company_name or ticker} trading in line with market",
            "Indian markets show mixed signals amid global cues"
        ]
        print("[News] Using fallback placeholder headlines.")

    # Score all headlines
    scores = [analyzer.polarity_scores(h)["compound"] for h in headlines]
    avg_score = sum(scores) / len(scores) if scores else 0

    if avg_score >= 0.05:
        sentiment = "Positive"
    elif avg_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "score": round(avg_score, 3),
        "headlines": headlines[:5],       # top 5 for the script
        "total_fetched": len(headlines)
    }
import os
import requests
import json

# ── LLM config ──────────────────────────────────────────────────────────────
# Option A: Groq (free, fast — recommended for hackathon)
#   Sign up at https://console.groq.com → get API key → set GROQ_API_KEY
# Option B: OpenAI
#   Set OPENAI_API_KEY instead
# Option C: Anthropic Claude
#   Set ANTHROPIC_API_KEY instead
# The function auto-detects whichever key is set.

GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


def _call_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-groq-8b-8192-tool-use-preview",   # fast and free
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 350,
        "temperature": 0.7
    }
    r = requests.post(url, headers=headers, json=body, timeout=15)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _call_openai(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 350,
        "temperature": 0.7
    }
    r = requests.post(url, headers=headers, json=body, timeout=15)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()
 

def _call_anthropic(prompt: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    body = {
        "model": "claude-haiku-4-5-20251001",   # fastest + cheapest
        "max_tokens": 350,
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, headers=headers, json=body, timeout=15)
    r.raise_for_status()
    return r.json()["content"][0]["text"].strip()


def _fallback_script(insight: dict) -> str:
    """Template fallback when no LLM key is configured."""
    stock = insight.get("stock", {})
    news  = insight.get("news", {})
    signal_emoji = "📈" if stock.get("signal") == "Bullish" else "📉" if stock.get("signal") == "Bearish" else "➡"

    return f"""Good morning, investors!

Here's your 60-second alpha for {stock.get('company_name', 'today')}.

{stock.get('company_name', 'The stock')} is trading at ₹{stock.get('price')}, 
{"above" if stock.get('price', 0) > stock.get('sma_20', 0) else "below"} its 20-day average of ₹{stock.get('sma_20')}.

The RSI stands at {stock.get('rsi')}, suggesting the stock is 
{"in overbought territory — caution advised" if stock.get('rsi', 50) > 70 else "oversold — watch for a bounce" if stock.get('rsi', 50) < 30 else "in a neutral zone"}.

News sentiment is {news.get('sentiment', 'Mixed').lower()}, with recent headlines pointing 
{"toward positive momentum" if news.get('sentiment') == 'Positive' else "to some headwinds" if news.get('sentiment') == 'Negative' else "in mixed directions"}.

Signal: {signal_emoji} {stock.get('signal', 'Neutral')}

Always do your own research before investing.
This is your AI-powered market insight."""


def generate_script(insight: dict) -> str:
    """
    Generate a 60-second market update script using an LLM.
    Falls back to a template if no API key is configured.
    """
    stock = insight.get("stock", {})
    news  = insight.get("news", {})

    prompt = f"""You are a sharp, energetic Indian financial news anchor.
Write a spoken 60-second market update video script for retail investors.

Data:
- Company: {stock.get('company_name')} ({stock.get('ticker')})
- Price: ₹{stock.get('price')} | 20-day SMA: ₹{stock.get('sma_20')}
- RSI: {stock.get('rsi')} | Signal: {stock.get('signal')}
- Volume: {stock.get('volume'):,} ({"above" if stock.get('volume', 0) > stock.get('avg_volume', 0) else "below"} average)
- News sentiment: {news.get('sentiment')} (score: {news.get('score')})
- Top headline: {news.get('headlines', [''])[0]}

Rules:
- Write ONLY the spoken script, no stage directions or brackets
- Start with a punchy hook line
- Mention the price, signal, and one key reason why
- End with a 1-line risk reminder
- Maximum 130 words
- Use Indian market context (NSE, rupees, retail investor perspective)
- Keep the tone confident but not reckless"""

    try:
        if GROQ_API_KEY:
            print("[Script] Using Groq LLM...")
            return _call_groq(prompt)
        elif ANTHROPIC_API_KEY:
            print("[Script] Using Anthropic Claude...")
            return _call_anthropic(prompt)
        elif OPENAI_API_KEY:
            print("[Script] Using OpenAI...")
            return _call_openai(prompt)
        else:
            print("[Script] No LLM key found — using template fallback.")
            return _fallback_script(insight)

    except Exception as e:
        print(f"[Script] LLM call failed: {e} — using template fallback.")
        return _fallback_script(insight)
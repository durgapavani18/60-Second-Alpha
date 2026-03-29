# 60-Second Alpha 📈

AI-powered 60-second market update video generator for Indian retail investors.
Built for the **ET Markets Hackathon** — AI for the Indian Investor.

---

## What it does

Enter any NSE stock ticker and get an auto-generated 60-second video with:
- Real-time stock price, SMA, RSI and signal (Bullish/Bearish/Neutral)
- Live news sentiment from ET Markets
- AI-written script (powered by Groq LLaMA)
- Text-to-speech voice narration
- Auto-generated video — zero human editing

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | FastAPI |
| Stock Data | yfinance (NSE) |
| News | ET Markets RSS / NewsAPI |
| Sentiment | VADER Sentiment |
| AI Script | Groq (LLaMA 3) |
| Voice | gTTS |
| Video | MoviePy |

---

## Project Structure

```
60sec-alpha/
├── app.py               # FastAPI server + UI
├── orchestrator.py      # Coordinates all agents
├── stock_agent.py       # Fetches NSE stock data + RSI
├── news_agent.py        # Fetches live news + sentiment
├── script_generator.py  # AI script via Groq LLM
├── voice_generator.py   # Text-to-speech
├── video_generator.py   # Renders final video
├── requirements.txt     # Python dependencies
├── .env                 # API keys (never commit this)
└── assets/
    ├── bg.jpg           # Video background image
    └── voice.mp3        # Generated audio (auto-created)
```

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/yourusername/60sec-alpha.git
cd 60sec-alpha
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get API keys

| Service | Free Tier | Link |
|---------|-----------|------|
| Groq | 100 req/day, very fast | console.groq.com |
| NewsAPI | 100 req/day | newsapi.org |

### 4. Create `.env` file

Create a file named `.env` in the project root:

```
GROQ_API_KEY=gsk_your_groq_key_here
NEWS_API_KEY=your_newsapi_key_here
```

> **Important:** Never commit your `.env` file to GitHub.

### 5. Run the server

```bash
uvicorn app:app --reload
```

Open your browser at `http://127.0.0.1:8000`

---

## Usage

1. Open `http://127.0.0.1:8000`
2. Enter an NSE ticker (e.g. `RELIANCE.NS`, `TCS.NS`, `INFY.NS`)
3. Click **Generate Video**
4. Wait 2-3 minutes for the video to render
5. Video downloads automatically

### Supported tickers (examples)

```
RELIANCE.NS    HDFCBANK.NS    TCS.NS
INFY.NS        WIPRO.NS       SBIN.NS
ICICIBANK.NS   ITC.NS         BAJFINANCE.NS
HINDUNILVR.NS
```

Any NSE ticker works — just add `.NS` suffix.

---

## How it works

```
User enters ticker
       ↓
stock_agent.py  →  Fetches price, SMA, RSI, volume from NSE via yfinance
news_agent.py   →  Fetches live headlines, runs VADER sentiment analysis
orchestrator.py →  Combines both into structured insight
script_generator.py → Groq LLaMA writes a 60-second spoken script
voice_generator.py  → gTTS converts script to MP3 audio
video_generator.py  → MoviePy renders text + audio into final MP4
       ↓
Video downloaded to browser
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for LLaMA script generation |
| `NEWS_API_KEY` | No | NewsAPI key (falls back to ET RSS if missing) |

---

## Known Limitations

- Video generation takes 2-3 minutes (MoviePy renders frame by frame)
- NewsAPI free tier limited to 100 requests/day
- Groq free tier limited to 100 requests/day
- Only supports NSE stocks (add `.NS` suffix)

---

## Roadmap (Phase 2)

- [ ] Candlestick chart embedded in video
- [ ] Animated signal badge (Bullish/Bearish overlay)
- [ ] Scrolling ticker tape at bottom
- [ ] RSI and MACD indicators
- [ ] FII/DII flow visualization

---

## Disclaimer

This tool is for educational purposes only. It does not constitute financial advice.
Always do your own research before making investment decisions.

---

Built with for the ET Markets Hackathon 2025

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from orchestrator import generate_insight
from script_generator import generate_script
from voice_generator import generate_voice
from video_generator import create_video

app = FastAPI(title="60-Second Alpha")

POPULAR_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "SBIN.NS", "WIPRO.NS", "HINDUNILVR.NS",
    "ITC.NS", "BAJFINANCE.NS"
]

@app.get("/", response_class=HTMLResponse)
def home():
    options_html = "\n".join(
        f'<option value="{t}">{t.replace(".NS", "")}</option>'
        for t in POPULAR_TICKERS
    )
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>60-Second Alpha</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #0a0a0f;
                color: #e8e8e8;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .card {{
                background: #13131a;
                border: 1px solid #2a2a3a;
                border-radius: 16px;
                padding: 40px;
                width: 420px;
                text-align: center;
            }}
            h1 {{ font-size: 28px; margin-bottom: 6px; color: #fff; }}
            p {{ color: #888; margin-bottom: 28px; font-size: 14px; }}
            label {{ display: block; text-align: left; font-size: 13px; color: #aaa; margin-bottom: 6px; }}
            input, select {{
                width: 100%;
                padding: 12px 16px;
                background: #1e1e2e;
                border: 1px solid #2a2a3a;
                border-radius: 8px;
                color: #fff;
                font-size: 15px;
                margin-bottom: 16px;
            }}
            input::placeholder {{ color: #555; }}
            button {{
                width: 100%;
                padding: 14px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            button:hover {{ background: #4338ca; }}
            .hint {{ font-size: 12px; color: #555; margin-top: 14px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📈 60-Second Alpha</h1>
            <p>AI-powered market video updates for Indian retail investors</p>
            <form action="/generate" method="post">
                <label>Enter NSE ticker or pick one:</label>
                <input
                    type="text"
                    name="stock"
                    placeholder="e.g. RELIANCE.NS, TCS.NS"
                    list="tickers"
                    required
                />
                <datalist id="tickers">
                    {options_html}
                </datalist>
                <button type="submit">Generate Video</button>
            </form>
            <p class="hint">Always add .NS suffix for NSE stocks (e.g. WIPRO.NS)</p>
        </div>
    </body>
    </html>
    """


@app.post("/generate")
def generate(stock: str = Form(...)):
    ticker = stock.strip().upper()
    if not ticker.endswith(".NS"):
        ticker = ticker + ".NS"

    insight = generate_insight(ticker=ticker)

    if not insight["success"]:
        raise HTTPException(status_code=400, detail=insight["error"])

    script = generate_script(insight)
    generate_voice(script)
    video_path = create_video(script)

    return FileResponse(video_path, media_type="video/mp4", filename=f"{ticker}_alpha.mp4")
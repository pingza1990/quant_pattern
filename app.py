import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from math import sqrt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantView",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

.stApp {
    background-color: #0d1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

/* Cards */
.metric-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
    font-family: 'DM Sans', sans-serif;
}

.metric-card .label {
    font-size: 11px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

.metric-card .value {
    font-family: 'Space Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #e6edf3;
}

.metric-card .sub {
    font-size: 11px;
    color: #8b949e;
    margin-top: 2px;
}

/* Signal box */
.signal-box {
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    border: 1px solid #30363d;
}

.signal-long {
    background-color: rgba(46, 160, 67, 0.12);
    border-color: #2ea043;
}

.signal-short {
    background-color: rgba(248, 81, 73, 0.12);
    border-color: #f85149;
}

.signal-neutral {
    background-color: rgba(88, 166, 255, 0.08);
    border-color: #58a6ff;
}

.signal-title {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.signal-long .signal-title  { color: #2ea043; }
.signal-short .signal-title { color: #f85149; }
.signal-neutral .signal-title { color: #58a6ff; }

.signal-meta {
    font-size: 12px;
    color: #8b949e;
    margin-bottom: 10px;
}

.signal-row {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    padding: 2px 0;
}

.signal-row .key { color: #8b949e; }
.signal-row .val { color: #e6edf3; font-weight: 600; }

.risk-high   { color: #f85149; }
.risk-medium { color: #d29922; }
.risk-low    { color: #2ea043; }

/* Conditions */
.condition-section {
    background-color: #0d1117;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 10px;
}

.condition-section .section-title {
    font-size: 10px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    font-family: 'DM Sans', sans-serif;
}

.condition-row {
    font-size: 11px;
    font-family: 'DM Sans', sans-serif;
    padding: 3px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

.cond-true-long  { color: #2ea043; }
.cond-true-short { color: #f85149; }
.cond-false      { color: #484f58; }

/* Pattern cards */
.pattern-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 6px;
    font-size: 12px;
}

.pattern-bullish { border-left: 3px solid #2ea043; }
.pattern-bearish { border-left: 3px solid #f85149; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #161b22;
    border-bottom: 1px solid #30363d;
    gap: 0;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #8b949e;
    border: none;
    padding: 10px 20px;
    font-size: 13px;
}

.stTabs [aria-selected="true"] {
    background-color: transparent;
    color: #e6edf3;
    border-bottom: 2px solid #58a6ff;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
}

/* Buttons */
.stButton > button {
    background-color: #21262d;
    border: 1px solid #30363d;
    color: #e6edf3;
    border-radius: 6px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    transition: all 0.2s;
}

.stButton > button:hover {
    background-color: #30363d;
    border-color: #58a6ff;
}

/* Divider */
hr {
    border-color: #21262d;
    margin: 12px 0;
}

/* Green/Red helpers */
.green { color: #2ea043; }
.red   { color: #f85149; }
.blue  { color: #58a6ff; }
.muted { color: #8b949e; }

.price-header {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
}

.ticker-label {
    font-size: 13px;
    color: #8b949e;
    margin-bottom: 2px;
}

.change-badge {
    font-family: 'Space Mono', monospace;
    font-size: 14px;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
}

.change-up   { background: rgba(46,160,67,0.15); color: #2ea043; }
.change-down { background: rgba(248,81,73,0.15); color: #f85149; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
THAI_POPULAR = ["PTT.BK", "ADVANC.BK", "AOT.BK", "CPALL.BK", "SCB.BK",
                "KBANK.BK", "BBL.BK", "TRUE.BK", "IVL.BK", "MINT.BK"]

US_POPULAR = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN",
              "SPY", "QQQ", "GOOGL", "META", "NFLX"]

# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCHING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_data(ticker, period, interval):
    try:
        df = yf.download(ticker, period=period, interval=interval,
                         auto_adjust=True, progress=False)
        if df is None or df.empty:
            return None
        # Flatten MultiIndex columns
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df.index = pd.to_datetime(df.index)
        return df
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# INDICATOR ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def compute_indicators(df):
    close  = df["Close"]
    high   = df["High"]
    low    = df["Low"]
    volume = df["Volume"]

    # Trend
    df["SMA20"]  = close.rolling(20).mean()
    df["SMA50"]  = close.rolling(50).mean()
    df["SMA200"] = close.rolling(200).mean()
    df["EMA9"]   = close.ewm(span=9, adjust=False).mean()
    df["EMA21"]  = close.ewm(span=21, adjust=False).mean()

    # Bollinger Bands
    df["BB_upper"] = df["SMA20"] + 2 * close.rolling(20).std()
    df["BB_lower"] = df["SMA20"] - 2 * close.rolling(20).std()

    # RSI (14)
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD (12, 26, 9)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["MACD"]        = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"]   = df["MACD"] - df["MACD_signal"]

    # ATR (14)
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low  - prev_close).abs(),
    ], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    # Volume SMA
    df["Vol_SMA20"] = volume.rolling(20).mean()

    return df


# ─────────────────────────────────────────────────────────────────────────────
# PATTERN DETECTION
# ─────────────────────────────────────────────────────────────────────────────
def detect_patterns(df):
    patterns = []
    n = len(df)
    if n < 10:
        return patterns

    close  = df["Close"].values
    open_  = df["Open"].values
    sma50  = df["SMA50"].values
    sma200 = df["SMA200"].values
    rsi    = df["RSI"].values
    dates  = df.index

    # 1 & 2 — Golden / Death Cross (full history)
    for i in range(1, n):
        s50_prev  = sma50[i-1]
        s200_prev = sma200[i-1]
        s50_cur   = sma50[i]
        s200_cur  = sma200[i]
        if any(np.isnan([s50_prev, s200_prev, s50_cur, s200_cur])):
            continue
        if s50_prev < s200_prev and s50_cur >= s200_cur:
            patterns.append({"type": "Golden Cross", "date": dates[i],
                              "price": close[i], "direction": "bullish", "confidence": 85})
        elif s50_prev > s200_prev and s50_cur <= s200_cur:
            patterns.append({"type": "Death Cross", "date": dates[i],
                              "price": close[i], "direction": "bearish", "confidence": 85})

    # 3 & 4 — Engulfing (last 30 bars)
    start = max(1, n - 30)
    for i in range(start, n):
        prev_open  = open_[i-1]
        prev_close = close[i-1]
        cur_open   = open_[i]
        cur_close  = close[i]

        prev_red   = prev_close < prev_open
        prev_green = prev_close > prev_open
        cur_green  = cur_close  > cur_open
        cur_red    = cur_close  < cur_open

        if prev_red and cur_green and cur_close > prev_open and cur_open < prev_close:
            patterns.append({"type": "Bullish Engulfing", "date": dates[i],
                              "price": cur_close, "direction": "bullish", "confidence": 72})
        elif prev_green and cur_red and cur_close < prev_open and cur_open > prev_close:
            patterns.append({"type": "Bearish Engulfing", "date": dates[i],
                              "price": cur_close, "direction": "bearish", "confidence": 72})

    # 5 — RSI Divergence (last 40 bars)
    if n >= 40:
        seg_close = close[-40:]
        seg_rsi   = rsi[-40:]
        if not np.isnan(seg_rsi[-1]) and not np.isnan(seg_rsi[-10]):
            if seg_close[-1] > seg_close[-10] and seg_rsi[-1] < seg_rsi[-10] and seg_rsi[-1] > 60:
                patterns.append({"type": "Bearish RSI Divergence", "date": dates[-1],
                                  "price": close[-1], "direction": "bearish", "confidence": 68})
            elif seg_close[-1] < seg_close[-10] and seg_rsi[-1] > seg_rsi[-10] and seg_rsi[-1] < 40:
                patterns.append({"type": "Bullish RSI Divergence", "date": dates[-1],
                                  "price": close[-1], "direction": "bullish", "confidence": 68})

    # Return max last 10
    return patterns[-10:]


# ─────────────────────────────────────────────────────────────────────────────
# PIVOT POINT HELPER
# ─────────────────────────────────────────────────────────────────────────────
def find_pivots(series, window=5):
    """Find local highs and lows using rolling window."""
    pivots_high = []
    pivots_low  = []
    for i in range(window, len(series) - window):
        window_vals = series.iloc[i - window : i + window + 1]
        if series.iloc[i] == window_vals.max():
            pivots_high.append((i, series.index[i], float(series.iloc[i])))
        if series.iloc[i] == window_vals.min():
            pivots_low.append((i, series.index[i], float(series.iloc[i])))
    return pivots_high, pivots_low


# ─────────────────────────────────────────────────────────────────────────────
# DIVERGENCE DETECTION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def detect_divergences(df, lookback_bars=10, pivot_window=5):
    """
    Detect all 4 divergence types using pivot-based RSI vs price comparison.
    Returns list of dicts with type, subtype, div_class, date, pivots,
    bars_ago, confidence, description.
    """
    results = []
    if len(df) < 20 or df["RSI"].isna().all():
        return results

    price = df["Close"]
    rsi   = df["RSI"].ffill()

    price_highs, price_lows = find_pivots(price, pivot_window)
    rsi_highs,   rsi_lows   = find_pivots(rsi,   pivot_window)

    def nearest_rsi_pivot(rsi_pivots, target_idx, tolerance=3):
        candidates = [
            (abs(r[0] - target_idx), r)
            for r in rsi_pivots
            if abs(r[0] - target_idx) <= tolerance
        ]
        if not candidates:
            return None
        return min(candidates, key=lambda x: x[0])[1]

    # ── REGULAR BULLISH: price Lower Low + RSI Higher Low ─────────────────
    for j in range(1, len(price_lows)):
        p2 = price_lows[j]        # more recent low
        p1 = price_lows[j - 1]    # earlier low
        if p2[0] - p1[0] < 5:
            continue
        r1 = nearest_rsi_pivot(rsi_lows, p1[0])
        r2 = nearest_rsi_pivot(rsi_lows, p2[0])
        if not r1 or not r2:
            continue
        if p2[2] < p1[2] and r2[2] > r1[2]:
            bars_ago = len(df) - 1 - p2[0]
            conf = 80
            if r2[2] < 40:          conf += 10
            if r2[2] - r1[2] > 5:  conf += 5
            conf = min(95, conf)
            results.append({
                "type": "Regular Bullish Divergence",
                "subtype": "bullish",
                "div_class": "regular",
                "date": p2[1],
                "price_pivot1": p1[2], "price_pivot2": p2[2],
                "rsi_pivot1": r1[2],   "rsi_pivot2": r2[2],
                "bars_ago": bars_ago,
                "confidence": conf,
                "description": (
                    f"Price made Lower Low ({p2[2]:.2f} < {p1[2]:.2f}) "
                    f"but RSI made Higher Low ({r2[2]:.1f} > {r1[2]:.1f})"
                ),
            })

    # ── HIDDEN BULLISH: price Higher Low + RSI Lower Low ──────────────────
    for j in range(1, len(price_lows)):
        p2 = price_lows[j]
        p1 = price_lows[j - 1]
        if p2[0] - p1[0] < 5:
            continue
        r1 = nearest_rsi_pivot(rsi_lows, p1[0])
        r2 = nearest_rsi_pivot(rsi_lows, p2[0])
        if not r1 or not r2:
            continue
        if p2[2] > p1[2] and r2[2] < r1[2]:
            bars_ago = len(df) - 1 - p2[0]
            conf = 72
            if r2[2] < 50: conf += 8
            conf = min(90, conf)
            results.append({
                "type": "Hidden Bullish Divergence",
                "subtype": "bullish",
                "div_class": "hidden",
                "date": p2[1],
                "price_pivot1": p1[2], "price_pivot2": p2[2],
                "rsi_pivot1": r1[2],   "rsi_pivot2": r2[2],
                "bars_ago": bars_ago,
                "confidence": conf,
                "description": (
                    f"Price made Higher Low ({p2[2]:.2f} > {p1[2]:.2f}) "
                    f"but RSI made Lower Low ({r2[2]:.1f} < {r1[2]:.1f})"
                ),
            })

    # ── REGULAR BEARISH: price Higher High + RSI Lower High ───────────────
    for j in range(1, len(price_highs)):
        p2 = price_highs[j]
        p1 = price_highs[j - 1]
        if p2[0] - p1[0] < 5:
            continue
        r1 = nearest_rsi_pivot(rsi_highs, p1[0])
        r2 = nearest_rsi_pivot(rsi_highs, p2[0])
        if not r1 or not r2:
            continue
        if p2[2] > p1[2] and r2[2] < r1[2]:
            bars_ago = len(df) - 1 - p2[0]
            conf = 80
            if r2[2] > 60:          conf += 10
            if r1[2] - r2[2] > 5:  conf += 5
            conf = min(95, conf)
            results.append({
                "type": "Regular Bearish Divergence",
                "subtype": "bearish",
                "div_class": "regular",
                "date": p2[1],
                "price_pivot1": p1[2], "price_pivot2": p2[2],
                "rsi_pivot1": r1[2],   "rsi_pivot2": r2[2],
                "bars_ago": bars_ago,
                "confidence": conf,
                "description": (
                    f"Price made Higher High ({p2[2]:.2f} > {p1[2]:.2f}) "
                    f"but RSI made Lower High ({r2[2]:.1f} < {r1[2]:.1f})"
                ),
            })

    # ── HIDDEN BEARISH: price Lower High + RSI Higher High ────────────────
    for j in range(1, len(price_highs)):
        p2 = price_highs[j]
        p1 = price_highs[j - 1]
        if p2[0] - p1[0] < 5:
            continue
        r1 = nearest_rsi_pivot(rsi_highs, p1[0])
        r2 = nearest_rsi_pivot(rsi_highs, p2[0])
        if not r1 or not r2:
            continue
        if p2[2] < p1[2] and r2[2] > r1[2]:
            bars_ago = len(df) - 1 - p2[0]
            conf = 72
            if r2[2] > 50: conf += 8
            conf = min(90, conf)
            results.append({
                "type": "Hidden Bearish Divergence",
                "subtype": "bearish",
                "div_class": "hidden",
                "date": p2[1],
                "price_pivot1": p1[2], "price_pivot2": p2[2],
                "rsi_pivot1": r1[2],   "rsi_pivot2": r2[2],
                "bars_ago": bars_ago,
                "confidence": conf,
                "description": (
                    f"Price made Lower High ({p2[2]:.2f} < {p1[2]:.2f}) "
                    f"but RSI made Higher High ({r2[2]:.1f} > {r1[2]:.1f})"
                ),
            })

    # Sort by date descending, then deduplicate signals within 3 calendar days
    results.sort(key=lambda x: x["date"], reverse=True)
    deduped    = []
    seen_dates = []
    for r in results:
        too_close = any(
            abs((r["date"] - d).days) <= 3
            for d in seen_dates
        )
        if not too_close:
            deduped.append(r)
            seen_dates.append(r["date"])

    return deduped


# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def compute_signal(df, min_conditions=3):
    if len(df) < 3:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    def _f(val):
        try:
            v = float(val)
            return v if pd.notna(v) else None
        except Exception:
            return None

    last_close    = _f(last["Close"])
    last_open     = _f(last["Open"])
    last_volume   = _f(last["Volume"])
    last_rsi      = _f(last["RSI"])
    last_MACD     = _f(last["MACD"])
    last_signal   = _f(last["MACD_signal"])
    last_EMA9     = _f(last["EMA9"])
    last_EMA21    = _f(last["EMA21"])
    last_SMA50    = _f(last["SMA50"])
    last_SMA200   = _f(last["SMA200"])
    last_BB_upper = _f(last["BB_upper"])
    last_BB_lower = _f(last["BB_lower"])
    last_Vol_SMA20= _f(last["Vol_SMA20"])
    last_ATR      = _f(last["ATR"])

    prev_rsi    = _f(prev["RSI"])
    prev_MACD   = _f(prev["MACD"])
    prev_signal = _f(prev["MACD_signal"])
    prev_EMA9   = _f(prev["EMA9"])
    prev_EMA21  = _f(prev["EMA21"])

    def _safe(val, default=False):
        return val if val is not None else default

    # LONG conditions
    conditions_long = {}

    cond = (prev_rsi is not None and last_rsi is not None and
            prev_rsi < 35 and last_rsi >= 30)
    conditions_long["RSI oversold recovery (RSI crossed 30↑)"] = bool(cond)

    cond = (last_close is not None and last_BB_lower is not None and
            last_close <= last_BB_lower * 1.02)
    conditions_long["Price near lower Bollinger Band"] = bool(cond)

    cond = (prev_MACD is not None and prev_signal is not None and
            last_MACD is not None and last_signal is not None and
            prev_MACD < prev_signal and last_MACD >= last_signal)
    conditions_long["MACD bullish crossover"] = bool(cond)

    cond = (prev_EMA9 is not None and prev_EMA21 is not None and
            last_EMA9 is not None and last_EMA21 is not None and
            prev_EMA9 < prev_EMA21 and last_EMA9 >= last_EMA21)
    conditions_long["EMA9 crossed above EMA21"] = bool(cond)

    cond = (last_close is not None and last_SMA50 is not None and
            last_close > last_SMA50)
    conditions_long["Price above SMA50"] = bool(cond)

    cond = (last_close is not None and last_SMA200 is not None and
            last_close > last_SMA200)
    conditions_long["Price above SMA200"] = bool(cond)

    cond = (last_close is not None and last_open is not None and
            last_volume is not None and last_Vol_SMA20 is not None and
            last_close > last_open and last_volume > last_Vol_SMA20 * 1.5)
    conditions_long["Volume spike on green candle"] = bool(cond)

    # SHORT conditions
    conditions_short = {}

    cond = (prev_rsi is not None and last_rsi is not None and
            prev_rsi > 65 and last_rsi <= 70)
    conditions_short["RSI overbought reversal (RSI crossed 70↓)"] = bool(cond)

    cond = (last_close is not None and last_BB_upper is not None and
            last_close >= last_BB_upper * 0.98)
    conditions_short["Price near upper Bollinger Band"] = bool(cond)

    cond = (prev_MACD is not None and prev_signal is not None and
            last_MACD is not None and last_signal is not None and
            prev_MACD > prev_signal and last_MACD <= last_signal)
    conditions_short["MACD bearish crossover"] = bool(cond)

    cond = (prev_EMA9 is not None and prev_EMA21 is not None and
            last_EMA9 is not None and last_EMA21 is not None and
            prev_EMA9 > prev_EMA21 and last_EMA9 <= last_EMA21)
    conditions_short["EMA9 crossed below EMA21"] = bool(cond)

    cond = (last_close is not None and last_SMA50 is not None and
            last_close < last_SMA50)
    conditions_short["Price below SMA50"] = bool(cond)

    cond = (last_close is not None and last_SMA200 is not None and
            last_close < last_SMA200)
    conditions_short["Price below SMA200"] = bool(cond)

    cond = (last_close is not None and last_open is not None and
            last_volume is not None and last_Vol_SMA20 is not None and
            last_close < last_open and last_volume > last_Vol_SMA20 * 1.5)
    conditions_short["Volume spike on red candle"] = bool(cond)

    # Score
    long_score  = sum(conditions_long.values())
    short_score = sum(conditions_short.values())

    if long_score >= min_conditions and long_score > short_score + 1:
        signal   = "LONG"
        strength = min(100, int(long_score / 7 * 100 + 10))
    elif short_score >= min_conditions and short_score > long_score + 1:
        signal   = "SHORT"
        strength = min(100, int(short_score / 7 * 100 + 10))
    else:
        signal   = "NEUTRAL"
        strength = 50

    # Risk levels
    price = last_close if last_close else 1.0
    atr   = last_ATR  if last_ATR  else 0.0
    atr_ratio = atr / price if price != 0 else 0
    if atr_ratio > 0.03:
        risk_level = "HIGH"
    elif atr_ratio > 0.015:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    entry = price
    if signal == "LONG":
        stop_loss   = entry - atr * 1.5
        take_profit = entry + atr * 3.0
    elif signal == "SHORT":
        stop_loss   = entry + atr * 1.5
        take_profit = entry - atr * 3.0
    else:
        stop_loss   = entry - atr * 1.5
        take_profit = entry + atr * 3.0

    return {
        "signal": signal,
        "strength": strength,
        "conditions_long": conditions_long,
        "conditions_short": conditions_short,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_level": risk_level,
        "rsi": last_rsi,
        "atr": atr,
        "atr_pct": atr_ratio * 100,
    }


# ─────────────────────────────────────────────────────────────────────────────
# BACKTESTING ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def run_backtest(df, initial_capital=100000):
    required = ["SMA50", "EMA9", "EMA21", "RSI", "MACD", "MACD_signal", "BB_upper", "BB_lower"]
    df2 = df.dropna(subset=required).copy()

    if len(df2) < 5:
        return None

    capital    = float(initial_capital)
    position   = 0
    entry_price= 0.0
    equity     = []
    trades     = []
    wins       = 0
    total_sells= 0

    closes      = df2["Close"].values
    opens_      = df2["Open"].values
    rsi_vals    = df2["RSI"].values
    macd_vals   = df2["MACD"].values
    sig_vals    = df2["MACD_signal"].values
    ema9_vals   = df2["EMA9"].values
    ema21_vals  = df2["EMA21"].values
    bb_upper    = df2["BB_upper"].values
    bb_lower    = df2["BB_lower"].values
    dates_bt    = df2.index

    for i in range(2, len(df2)):
        price   = float(closes[i])
        prev_i  = i - 1

        prev_rsi    = float(rsi_vals[prev_i])
        curr_rsi    = float(rsi_vals[i])
        prev_macd   = float(macd_vals[prev_i])
        curr_macd   = float(macd_vals[i])
        prev_msig   = float(sig_vals[prev_i])
        curr_msig   = float(sig_vals[i])
        prev_ema9   = float(ema9_vals[prev_i])
        curr_ema9   = float(ema9_vals[i])
        prev_ema21  = float(ema21_vals[prev_i])
        curr_ema21  = float(ema21_vals[i])
        curr_bbu    = float(bb_upper[i])
        curr_bbl    = float(bb_lower[i])

        long_score = 0
        if prev_rsi < 35:
            long_score += 1
        if price <= curr_bbl * 1.02:
            long_score += 1
        if prev_macd < prev_msig and curr_macd >= curr_msig:
            long_score += 1
        if prev_ema9 < prev_ema21 and curr_ema9 >= curr_ema21:
            long_score += 1

        short_score = 0
        if prev_rsi > 65:
            short_score += 1
        if price >= curr_bbu * 0.98:
            short_score += 1
        if prev_macd > prev_msig and curr_macd <= curr_msig:
            short_score += 1
        if prev_ema9 > prev_ema21 and curr_ema9 <= curr_ema21:
            short_score += 1

        # EXIT
        if position > 0 and (short_score >= 2 or curr_rsi > 70):
            pnl = (price - entry_price) * position
            capital += position * price
            trades.append({
                "date": dates_bt[i],
                "type": "SELL",
                "price": price,
                "shares": position,
                "pnl": pnl,
            })
            total_sells += 1
            if pnl > 0:
                wins += 1
            position = 0
            entry_price = 0.0

        # ENTRY
        elif position == 0 and long_score >= 2 and capital > price:
            shares = int(capital * 0.95 / price)
            if shares > 0:
                capital -= shares * price
                position = shares
                entry_price = price
                trades.append({
                    "date": dates_bt[i],
                    "type": "BUY",
                    "price": price,
                    "shares": shares,
                    "pnl": None,
                })

        equity.append(capital + position * price)

    # Force-close
    if position > 0:
        last_price = float(closes[-1])
        pnl = (last_price - entry_price) * position
        capital += position * last_price
        trades.append({
            "date": dates_bt.iloc[-1] if hasattr(dates_bt, 'iloc') else dates_bt[-1],
            "type": "SELL",
            "price": last_price,
            "shares": position,
            "pnl": pnl,
        })
        total_sells += 1
        if pnl > 0:
            wins += 1
        position = 0

    if not equity:
        return None

    final_capital = capital + position * float(closes[-1])
    equity_series = pd.Series(equity, index=df2.index[2:2 + len(equity)])
    returns = equity_series.pct_change().dropna()

    total_return = (final_capital - initial_capital) / initial_capital * 100
    win_rate     = (wins / total_sells * 100) if total_sells > 0 else 0.0
    total_trades = len([t for t in trades if t["type"] == "BUY"])

    if len(returns) > 1 and returns.std() != 0:
        sharpe = float(returns.mean() / returns.std() * sqrt(252))
    else:
        sharpe = 0.0

    running_max  = equity_series.cummax()
    drawdown     = (equity_series - running_max) / running_max.replace(0, np.nan) * 100
    max_drawdown = float(drawdown.min()) if len(drawdown) > 0 else 0.0

    return {
        "total_return": total_return,
        "win_rate": win_rate,
        "total_trades": total_trades,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "equity_curve": equity_series,
        "trades": trades,
        "final_capital": final_capital,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHART: MAIN
# ─────────────────────────────────────────────────────────────────────────────
def make_main_chart(df, patterns, show_sma20, show_sma50, show_sma200,
                    show_ema, show_bb, div_signals=None):
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.2, 0.2],
        vertical_spacing=0.02,
        specs=[[{"secondary_y": True}],
               [{"secondary_y": False}],
               [{"secondary_y": False}]],
    )

    # Candlestick colors
    candle_colors_up   = ["#2ea043"] * len(df)
    candle_colors_down = ["#f85149"] * len(df)
    vol_colors = ["#2ea043" if c >= o else "#f85149"
                  for c, o in zip(df["Close"], df["Open"])]

    # Row 1 — Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        increasing_line_color="#2ea043",
        decreasing_line_color="#f85149",
        name="Price",
    ), row=1, col=1, secondary_y=False)

    # Volume bars on secondary y
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"],
        marker_color=vol_colors,
        opacity=0.3, name="Volume", showlegend=False,
    ), row=1, col=1, secondary_y=True)

    # Moving averages
    if show_sma20 and "SMA20" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMA20"],
            line=dict(color="#f0e68c", width=1),
            name="SMA20",
        ), row=1, col=1, secondary_y=False)

    if show_sma50 and "SMA50" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMA50"],
            line=dict(color="#87ceeb", width=1.5),
            name="SMA50",
        ), row=1, col=1, secondary_y=False)

    if show_sma200 and "SMA200" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["SMA200"],
            line=dict(color="#ff8c69", width=1.5),
            name="SMA200",
        ), row=1, col=1, secondary_y=False)

    if show_ema and "EMA9" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["EMA9"],
            line=dict(color="#98fb98", width=1, dash="dot"),
            name="EMA9",
        ), row=1, col=1, secondary_y=False)

    if show_ema and "EMA21" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["EMA21"],
            line=dict(color="#dda0dd", width=1, dash="dot"),
            name="EMA21",
        ), row=1, col=1, secondary_y=False)

    if show_bb and "BB_upper" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_upper"],
            line=dict(color="#58a6ff", width=1, dash="dash"),
            name="BB Upper",
        ), row=1, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_lower"],
            line=dict(color="#58a6ff", width=1, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(88,166,255,0.05)",
            name="BB Lower",
        ), row=1, col=1, secondary_y=False)

    # Pattern markers
    bull_pats = [p for p in patterns if p["direction"] == "bullish"]
    bear_pats = [p for p in patterns if p["direction"] == "bearish"]

    if bull_pats:
        fig.add_trace(go.Scatter(
            x=[p["date"] for p in bull_pats],
            y=[p["price"] * 0.985 for p in bull_pats],
            mode="markers+text",
            marker=dict(symbol="triangle-up", color="#2ea043", size=12),
            text=[p["type"] for p in bull_pats],
            textposition="bottom center",
            textfont=dict(color="#2ea043", size=9),
            name="Bullish Pattern",
            showlegend=False,
        ), row=1, col=1, secondary_y=False)

    if bear_pats:
        fig.add_trace(go.Scatter(
            x=[p["date"] for p in bear_pats],
            y=[p["price"] * 1.015 for p in bear_pats],
            mode="markers+text",
            marker=dict(symbol="triangle-down", color="#f85149", size=12),
            text=[p["type"] for p in bear_pats],
            textposition="top center",
            textfont=dict(color="#f85149", size=9),
            name="Bearish Pattern",
            showlegend=False,
        ), row=1, col=1, secondary_y=False)

    # Row 2 — RSI
    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"],
        line=dict(color="#c9a832", width=1.5),
        name="RSI",
    ), row=2, col=1)

    fig.add_hline(y=70, line_color="#f85149", line_dash="dash",
                  line_width=1, row=2, col=1)
    fig.add_hline(y=30, line_color="#2ea043", line_dash="dash",
                  line_width=1, row=2, col=1)
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(248,81,73,0.07)",
                  line_width=0, row=2, col=1)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(46,160,67,0.07)",
                  line_width=0, row=2, col=1)

    # Row 3 — MACD
    macd_colors = ["#2ea043" if v >= 0 else "#f85149"
                   for v in df["MACD_hist"].fillna(0)]

    fig.add_trace(go.Bar(
        x=df.index, y=df["MACD_hist"],
        marker_color=macd_colors,
        opacity=0.6, name="MACD Hist", showlegend=False,
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD"],
        line=dict(color="#58a6ff", width=1.5),
        name="MACD",
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD_signal"],
        line=dict(color="#f0a500", width=1.5),
        name="Signal",
    ), row=3, col=1)

    # Layout
    fig.update_layout(
        height=700,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", family="DM Sans"),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
            font=dict(size=11), orientation="h",
            yanchor="bottom", y=1.01, xanchor="left", x=0,
        ),
        showlegend=True,
    )

    grid_style = dict(gridcolor="#21262d", zerolinecolor="#21262d")
    fig.update_xaxes(**grid_style)
    fig.update_yaxes(**grid_style)

    # Secondary y (volume) — hide labels
    fig.update_yaxes(showticklabels=False, row=1, col=1, secondary_y=True)

    # Divergence annotations on RSI panel (row 2)
    if div_signals:
        for dv in div_signals:
            dv_color = "#2ea043" if dv["subtype"] == "bullish" else "#f85149"
            try:
                dv_date = dv["date"]
                fig.add_vline(
                    x=dv_date,
                    line=dict(color=dv_color, width=1, dash="dot"),
                    row=2, col=1,
                )
                # Add a small marker on the RSI line at signal date
                rsi_at_date = None
                try:
                    idx = df.index.get_indexer([dv_date], method="nearest")[0]
                    rsi_at_date = float(df["RSI"].iloc[idx])
                except Exception:
                    pass
                if rsi_at_date is not None:
                    marker_sym = "triangle-up" if dv["subtype"] == "bullish" else "triangle-down"
                    fig.add_trace(go.Scatter(
                        x=[dv_date],
                        y=[rsi_at_date],
                        mode="markers",
                        marker=dict(symbol=marker_sym, color=dv_color,
                                    size=9, line=dict(width=1, color="#0d1117")),
                        name=dv["type"],
                        showlegend=False,
                        hovertemplate=(
                            f"<b>{dv['type']}</b><br>"
                            f"Conf: {dv['confidence']}%<br>"
                            f"RSI: {rsi_at_date:.1f}<extra></extra>"
                        ),
                    ), row=2, col=1)
            except Exception:
                pass

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# CHART: EQUITY
# ─────────────────────────────────────────────────────────────────────────────
def make_equity_chart(bt_result):
    eq   = bt_result["equity_curve"]
    trs  = bt_result["trades"]

    buy_dates  = [t["date"] for t in trs if t["type"] == "BUY"]
    sell_dates = [t["date"] for t in trs if t["type"] == "SELL"]
    buy_vals   = [eq.asof(d) if hasattr(eq, 'asof') else eq.iloc[0] for d in buy_dates]
    sell_vals  = [eq.asof(d) if hasattr(eq, 'asof') else eq.iloc[0] for d in sell_dates]

    # Better approach: map dates to equity values
    buy_vals  = []
    sell_vals = []
    for d in buy_dates:
        try:
            idx = eq.index.get_indexer([d], method="nearest")[0]
            buy_vals.append(float(eq.iloc[idx]))
        except Exception:
            buy_vals.append(float(eq.iloc[0]))
    for d in sell_dates:
        try:
            idx = eq.index.get_indexer([d], method="nearest")[0]
            sell_vals.append(float(eq.iloc[idx]))
        except Exception:
            sell_vals.append(float(eq.iloc[0]))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=eq.index, y=eq.values,
        line=dict(color="#58a6ff", width=2),
        fill="tozeroy",
        fillcolor="rgba(88,166,255,0.08)",
        name="Equity",
    ))

    if buy_dates:
        fig.add_trace(go.Scatter(
            x=buy_dates, y=buy_vals,
            mode="markers",
            marker=dict(symbol="triangle-up", size=10, color="#2ea043"),
            name="BUY",
        ))

    if sell_dates:
        fig.add_trace(go.Scatter(
            x=sell_dates, y=sell_vals,
            mode="markers",
            marker=dict(symbol="triangle-down", size=10, color="#f85149"),
            name="SELL",
        ))

    fig.update_layout(
        height=350,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#8b949e", family="DM Sans"),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
                    font=dict(size=11)),
    )
    fig.update_xaxes(gridcolor="#21262d", zerolinecolor="#21262d")
    fig.update_yaxes(gridcolor="#21262d", zerolinecolor="#21262d")

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL BADGE HELPER
# ─────────────────────────────────────────────────────────────────────────────
def signal_badge(signal, strength):
    _color = {"LONG": "#2ea043", "SHORT": "#f85149", "NEUTRAL": "#8b949e"}.get(signal, "#8b949e")
    _emoji = {"LONG": "🟢",      "SHORT": "🔴",       "NEUTRAL": "⚪"}.get(signal, "⚪")
    _rgb   = {"LONG": "46,160,67","SHORT": "248,81,73","NEUTRAL": "139,148,158"}.get(signal, "139,148,158")
    return (
        f"<span style='"
        f"background:rgba({_rgb},0.15);"
        f"color:{_color};"
        f"border:1px solid {_color};"
        f"border-radius:6px;"
        f"padding:2px 10px;"
        f"font-family:Space Mono,monospace;"
        f"font-size:0.8rem;"
        f"font-weight:700'>"
        f"{_emoji} {signal} {strength}"
        f"</span>"
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 QuantView")
    st.markdown("---")

    market = st.radio("Market", ["🇹🇭 Thai (.BK)", "🇺🇸 US", "Manual input"])

    if market == "🇹🇭 Thai (.BK)":
        ticker = st.selectbox("Symbol", THAI_POPULAR)
    elif market == "🇺🇸 US":
        ticker = st.selectbox("Symbol", US_POPULAR)
    else:
        raw = st.text_input("Enter ticker symbol", value="AAPL")
        ticker = raw.strip().upper()

    currency = "THB" if ticker.endswith(".BK") else "USD"
    curr_sym = "฿" if currency == "THB" else "$"

    period = st.select_slider(
        "Period",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        value="6mo",
    )

    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

    st.markdown("---")
    st.markdown("**Indicators**")
    show_sma20  = st.checkbox("SMA 20",          value=True)
    show_sma50  = st.checkbox("SMA 50",          value=True)
    show_sma200 = st.checkbox("SMA 200",         value=True)
    show_ema    = st.checkbox("EMA 9 / 21",      value=True)
    show_bb     = st.checkbox("Bollinger Bands", value=True)

    st.markdown("---")
    bt_capital = st.number_input(
        "Initial Backtest Capital",
        min_value=1000,
        value=100000,
        step=10000,
        format="%d",
    )

    st.markdown("---")
    st.markdown("**🎯 Signal Filter**")

    signal_filter = st.multiselect(
        "Show signals",
        options=["LONG", "NEUTRAL", "SHORT"],
        default=["LONG", "NEUTRAL", "SHORT"],
    )

    risk_filter = st.multiselect(
        "Risk level",
        options=["LOW", "MEDIUM", "HIGH"],
        default=["LOW", "MEDIUM", "HIGH"],
    )

    st.markdown("**⚙️ Signal Sensitivity**")
    min_strength = st.slider(
        "Minimum signal strength",
        min_value=0, max_value=100, value=0, step=5,
        help="Only show signals at or above this strength",
    )
    min_conditions = st.slider(
        "Min conditions required",
        min_value=1, max_value=7, value=3, step=1,
        help="How many conditions must be met to trigger LONG or SHORT",
    )

    st.markdown("---")
    st.markdown("**🔀 Divergence Scanner**")

    div_types = st.multiselect(
        "Divergence types",
        options=[
            "Regular Bullish Divergence",
            "Hidden Bullish Divergence",
            "Regular Bearish Divergence",
            "Hidden Bearish Divergence",
        ],
        default=["Regular Bullish Divergence", "Hidden Bullish Divergence"],
        help="Regular = reversal signal | Hidden = continuation signal",
    )

    max_bars_ago = st.slider(
        "Signal occurred within last N bars",
        min_value=1, max_value=60, value=10, step=1,
        help="Only show divergences detected within this many bars from today",
    )

    min_div_confidence = st.slider(
        "Min divergence confidence",
        min_value=50, max_value=95, value=70, step=5,
    )

    pivot_window = st.slider(
        "Pivot sensitivity (bars)",
        min_value=3, max_value=10, value=5, step=1,
        help="Smaller = more sensitive (more signals), Larger = fewer but stronger signals",
    )

    div_scan_period = st.selectbox(
        "Scan period",
        ["3mo", "6mo", "1y"],
        index=1,
        key="div_scan_period",
    )

    st.caption("Data: Yahoo Finance · Cached 5 min")

# ─────────────────────────────────────────────────────────────────────────────
# GUARD: empty ticker
# ─────────────────────────────────────────────────────────────────────────────
if not ticker:
    st.info("Please enter a ticker symbol in the sidebar.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# FETCH + COMPUTE
# ─────────────────────────────────────────────────────────────────────────────
df_raw = fetch_data(ticker, period, interval)

if df_raw is None or df_raw.empty:
    st.error(f"Could not fetch data for **{ticker}**. Check the symbol and try again.")
    st.stop()

df = compute_indicators(df_raw.copy())
patterns = detect_patterns(df)
sig = compute_signal(df, min_conditions)

# Price summary
last_close = float(df["Close"].iloc[-1]) if pd.notna(df["Close"].iloc[-1]) else 0.0
prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 and pd.notna(df["Close"].iloc[-2]) else last_close
price_change    = last_close - prev_close
price_change_pct = (price_change / prev_close * 100) if prev_close != 0 else 0.0

# ─────────────────────────────────────────────────────────────────────────────
# PORTFOLIO SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state["portfolio"] = []

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Chart & Signal", "⏱ Backtesting",
    "💼 Portfolio Tracker", "📋 Scanner", "🔀 Divergence",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — Chart & Signal
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([3, 1])

    with col_left:
        # Header
        chg_class = "change-up" if price_change >= 0 else "change-down"
        chg_arrow = "▲" if price_change >= 0 else "▼"
        badge_html = signal_badge(sig["signal"], sig["strength"]) if sig else ""
        st.markdown(f"""
        <div class="ticker-label">
            {ticker} &nbsp;·&nbsp; {period} &nbsp;·&nbsp; {interval}
        </div>
        <div style="display:flex; align-items:baseline; gap:12px; margin-bottom:12px; flex-wrap:wrap;">
            <span class="price-header">{curr_sym}{last_close:,.2f}</span>
            <span class="change-badge {chg_class}">
                {chg_arrow} {abs(price_change):,.2f} ({abs(price_change_pct):.2f}%)
            </span>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)

        # Divergence detection for current ticker
        divs = detect_divergences(df, lookback_bars=max_bars_ago,
                                   pivot_window=pivot_window)
        recent_divs = [
            d for d in divs
            if d["bars_ago"] <= max_bars_ago
            and d["type"] in div_types
            and d["confidence"] >= min_div_confidence
        ]

        # Main chart (with divergence annotations on RSI panel)
        fig_main = make_main_chart(
            df, patterns,
            show_sma20, show_sma50, show_sma200, show_ema, show_bb,
            div_signals=recent_divs,
        )
        st.plotly_chart(fig_main, use_container_width=True)

        # Patterns
        if patterns:
            recent = patterns[-4:]
            st.markdown("**Detected Patterns**")
            pat_cols = st.columns(len(recent))
            for i, pat in enumerate(recent):
                with pat_cols[i]:
                    dir_class = "pattern-bullish" if pat["direction"] == "bullish" else "pattern-bearish"
                    dir_color = "#2ea043" if pat["direction"] == "bullish" else "#f85149"
                    dir_emoji = "▲" if pat["direction"] == "bullish" else "▼"
                    try:
                        date_str = pat["date"].strftime("%Y-%m-%d")
                    except Exception:
                        date_str = str(pat["date"])[:10]
                    st.markdown(f"""
                    <div class="pattern-card {dir_class}">
                        <div style="color:{dir_color}; font-weight:600; font-size:12px;">
                            {dir_emoji} {pat['type']}
                        </div>
                        <div class="muted" style="font-size:11px;">{date_str}</div>
                        <div style="font-size:11px;">
                            Confidence: <strong>{pat['confidence']}%</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Divergence signals panel
        if recent_divs:
            st.markdown("---")
            st.markdown("**🔀 Divergence Signals**")
            for d in recent_divs[:5]:
                color     = "#2ea043" if d["subtype"] == "bullish" else "#f85149"
                cls_badge = "🔄 Regular" if d["div_class"] == "regular" else "↗️ Hidden"
                try:
                    sig_date = d["date"].strftime("%Y-%m-%d")
                except Exception:
                    sig_date = str(d["date"])[:10]
                st.markdown(f"""
                <div style='background:#161b22;border:1px solid {color}33;
                            border-left:3px solid {color};border-radius:8px;
                            padding:12px 16px;margin-bottom:8px'>
                    <div style='display:flex;justify-content:space-between;align-items:center'>
                        <span style='color:{color};font-weight:700;font-size:0.9rem'>
                            {d["type"]}
                        </span>
                        <span style='color:#8b949e;font-size:0.78rem'>
                            {cls_badge} &nbsp;·&nbsp; {d["confidence"]}% conf
                            &nbsp;·&nbsp; {d["bars_ago"]} bars ago
                        </span>
                    </div>
                    <div style='color:#8b949e;font-size:0.8rem;margin-top:6px'>
                        {d["description"]}
                    </div>
                    <div style='color:#8b949e;font-size:0.75rem;margin-top:4px'>
                        📅 {sig_date}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        if sig is None:
            st.warning("Not enough data to compute signal.")
        else:
            s        = sig["signal"]
            strength = sig["strength"]
            rl       = sig["risk_level"]

            # ── Signal gate ──────────────────────────────────────────────────
            signal_blocked = (
                s not in signal_filter or
                rl not in risk_filter or
                strength < min_strength
            )

            if signal_blocked:
                st.markdown(f"""
                <div class="signal-box signal-neutral">
                    <div style="font-size:1.1rem;font-weight:700">🚫 FILTERED OUT</div>
                    <div style="color:#8b949e;font-size:0.85rem;margin-top:8px">
                        Signal: {s} &nbsp;·&nbsp; Strength: {strength}/100 &nbsp;·&nbsp; Risk: {rl}
                    </div>
                    <div style="color:#8b949e;font-size:0.8rem;margin-top:4px">
                        Does not match your current filter settings
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if s == "LONG":
                    box_class = "signal-long"
                    sig_emoji = "🟢"
                elif s == "SHORT":
                    box_class = "signal-short"
                    sig_emoji = "🔴"
                else:
                    box_class = "signal-neutral"
                    sig_emoji = "⚪"

                entry_fmt = f"{curr_sym}{sig['entry']:,.2f}"
                sl_fmt    = f"{curr_sym}{sig['stop_loss']:,.2f}"
                tp_fmt    = f"{curr_sym}{sig['take_profit']:,.2f}"
                rl_class  = f"risk-{rl.lower()}"

                st.markdown(f"""
                <div class="signal-box {box_class}">
                    <div class="signal-title">{sig_emoji} {s}</div>
                    <div class="signal-meta">Signal Strength: {strength}/100</div>
                    <div class="signal-row">
                        <span class="key">📍 Entry</span>
                        <span class="val">{entry_fmt}</span>
                    </div>
                    <div class="signal-row">
                        <span class="key">🛑 Stop</span>
                        <span class="val">{sl_fmt}</span>
                    </div>
                    <div class="signal-row">
                        <span class="key">🎯 Target</span>
                        <span class="val">{tp_fmt}</span>
                    </div>
                    <div class="signal-row" style="margin-top:6px;">
                        <span class="key">Risk</span>
                        <span class="val {rl_class}">{rl}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Conditions (always shown, read-only reference) ───────────────
            long_rows_html = ""
            for name, val in sig["conditions_long"].items():
                short_name = name.split("(")[0].strip()
                if val:
                    long_rows_html += f'<div class="condition-row cond-true-long">✅ {short_name}</div>'
                else:
                    long_rows_html += f'<div class="condition-row cond-false">❌ {short_name}</div>'

            st.markdown(f"""
            <div class="condition-section">
                <div class="section-title">🟢 Long Conditions ({sum(sig['conditions_long'].values())}/7)</div>
                {long_rows_html}
            </div>
            """, unsafe_allow_html=True)

            short_rows_html = ""
            for name, val in sig["conditions_short"].items():
                short_name = name.split("(")[0].strip()
                if val:
                    short_rows_html += f'<div class="condition-row cond-true-short">✅ {short_name}</div>'
                else:
                    short_rows_html += f'<div class="condition-row cond-false">❌ {short_name}</div>'

            st.markdown(f"""
            <div class="condition-section">
                <div class="section-title">🔴 Short Conditions ({sum(sig['conditions_short'].values())}/7)</div>
                {short_rows_html}
            </div>
            """, unsafe_allow_html=True)

            # RSI card
            rsi_val = sig.get("rsi")
            if rsi_val is not None:
                if rsi_val > 70:
                    rsi_color = "#f85149"
                    rsi_label = "Overbought"
                elif rsi_val < 30:
                    rsi_color = "#2ea043"
                    rsi_label = "Oversold"
                else:
                    rsi_color = "#d29922"
                    rsi_label = "Neutral"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">RSI (14) · {rsi_label}</div>
                    <div class="value" style="color:{rsi_color};">{rsi_val:.1f}</div>
                </div>
                """, unsafe_allow_html=True)

            # ATR card
            atr_val = sig.get("atr", 0)
            atr_pct = sig.get("atr_pct", 0)
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">ATR (14)</div>
                <div class="value">{curr_sym}{atr_val:,.2f}</div>
                <div class="sub">({atr_pct:.1f}% of price)</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # Portfolio add
            qty_input = st.number_input("Qty", min_value=1, value=100, key="qty_input")
            if st.button(f"➕ Add {ticker} to Portfolio"):
                st.session_state["portfolio"].append({
                    "ticker":   ticker,
                    "qty":      qty_input,
                    "entry":    last_close,
                    "currency": currency,
                    "added":    pd.Timestamp.now().strftime("%Y-%m-%d"),
                })
                st.success(f"Added {qty_input}x {ticker} @ {curr_sym}{last_close:,.2f}")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — Backtesting
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"### Backtest: **{ticker}** · {period} · {interval}")
    st.caption(
        "Strategy: buy on 2+ bullish signals (RSI oversold, near lower BB, "
        "MACD/EMA crossovers), sell on 2+ bearish reversal signals or RSI > 70."
    )

    bt = run_backtest(df, initial_capital=int(bt_capital))

    if bt is None:
        st.warning("Insufficient data for backtesting (need at least 5 valid bars after indicator warmup).")
    else:
        # Metric cards
        m1, m2, m3, m4, m5 = st.columns(5)

        ret_color = "#2ea043" if bt["total_return"] >= 0 else "#f85149"
        ret_sign  = "+" if bt["total_return"] >= 0 else ""

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Return</div>
                <div class="value" style="color:{ret_color};">{ret_sign}{bt['total_return']:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Win Rate</div>
                <div class="value">{bt['win_rate']:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Trades</div>
                <div class="value">{bt['total_trades']}</div>
            </div>""", unsafe_allow_html=True)

        sharpe_color = ("#2ea043" if bt["sharpe"] > 1 else
                        "#d29922" if bt["sharpe"] > 0 else "#f85149")
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Sharpe Ratio</div>
                <div class="value" style="color:{sharpe_color};">{bt['sharpe']:.2f}</div>
            </div>""", unsafe_allow_html=True)

        dd_color = "#f85149" if bt["max_drawdown"] < -10 else "#d29922"
        with m5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Max Drawdown</div>
                <div class="value" style="color:{dd_color};">{bt['max_drawdown']:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        # Equity chart
        fig_eq = make_equity_chart(bt)
        st.plotly_chart(fig_eq, use_container_width=True)

        # Comparison cards
        c1, c2 = st.columns(2)

        with c1:
            fc = bt["final_capital"]
            fc_color = "#2ea043" if fc >= bt_capital else "#f85149"
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Final Capital</div>
                <div class="value" style="color:{fc_color};">{curr_sym}{fc:,.0f}</div>
                <div class="sub">Started with {curr_sym}{bt_capital:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        with c2:
            # Buy & hold benchmark
            first_close = float(df["Close"].dropna().iloc[0])
            bh_return   = (last_close - first_close) / first_close * 100 if first_close != 0 else 0.0
            bh_color    = "#2ea043" if bh_return >= 0 else "#f85149"
            bh_sign     = "+" if bh_return >= 0 else ""
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Buy &amp; Hold Benchmark</div>
                <div class="value" style="color:{bh_color};">{bh_sign}{bh_return:.1f}%</div>
                <div class="sub">vs Strategy: {ret_sign}{bt['total_return']:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        # Trade log
        if bt["trades"]:
            st.markdown("**Trade Log**")
            trade_rows = []
            for t in bt["trades"]:
                try:
                    d_str = t["date"].strftime("%Y-%m-%d")
                except Exception:
                    d_str = str(t["date"])[:10]
                pnl = t.get("pnl")
                if pnl is None:
                    pnl_str = "-"
                else:
                    pnl_str = f"+{pnl:,.2f}" if pnl >= 0 else f"{pnl:,.2f}"
                trade_rows.append({
                    "Date":   d_str,
                    "Type":   t["type"],
                    "Price":  f"{curr_sym}{t['price']:,.2f}",
                    "Shares": t["shares"],
                    "P&L":    pnl_str,
                })
            trade_df = pd.DataFrame(trade_rows)
            st.dataframe(trade_df, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — Portfolio Tracker
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Portfolio Tracker")

    portfolio = st.session_state["portfolio"]

    if not portfolio:
        st.info("No positions yet. Add tickers from the Chart & Signal tab.")
    else:
        # Fetch current prices
        rows = []
        for pos in portfolio:
            tk   = pos["ticker"]
            qty  = pos["qty"]
            ep   = pos["entry"]
            cur  = pos["currency"]
            cs   = "฿" if cur == "THB" else "$"
            sym  = "฿" if cur == "THB" else "$"
            added= pos.get("added", "")

            pdata = fetch_data(tk, "5d", "1d")
            if pdata is not None and not pdata.empty:
                cur_price = float(pdata["Close"].dropna().iloc[-1])
            else:
                cur_price = ep  # fallback

            cost  = ep * qty
            value = cur_price * qty
            pnl   = value - cost
            pnlp  = pnl / cost * 100 if cost != 0 else 0.0

            rows.append({
                "Ticker":   tk,
                "Qty":      qty,
                "Entry":    f"{sym}{ep:,.2f}",
                "Current":  f"{sym}{cur_price:,.2f}",
                "Cost":     f"{sym}{cost:,.0f}",
                "Value":    f"{sym}{value:,.0f}",
                "P&L":      f"+{pnl:,.0f}" if pnl >= 0 else f"{pnl:,.0f}",
                "P&L%":     f"+{pnlp:.1f}%" if pnlp >= 0 else f"{pnlp:.1f}%",
                "Currency": cur,
                "Added":    added,
                # raw for summary
                "_value": value,
                "_pnl":   pnl,
                "_cost":  cost,
            })

        # Summary
        total_value  = sum(r["_value"] for r in rows)
        total_pnl    = sum(r["_pnl"]   for r in rows)
        total_cost   = sum(r["_cost"]  for r in rows)
        total_ret_p  = total_pnl / total_cost * 100 if total_cost != 0 else 0.0
        pnl_color    = "#2ea043" if total_pnl >= 0 else "#f85149"
        pnl_sign     = "+" if total_pnl >= 0 else ""

        sm1, sm2, sm3 = st.columns(3)
        with sm1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Value</div>
                <div class="value">{total_value:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with sm2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total P&amp;L</div>
                <div class="value" style="color:{pnl_color};">{pnl_sign}{total_pnl:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with sm3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Return</div>
                <div class="value" style="color:{pnl_color};">{pnl_sign}{total_ret_p:.1f}%</div>
            </div>""", unsafe_allow_html=True)

        # Table
        display_rows = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
        port_df = pd.DataFrame(display_rows)
        st.dataframe(port_df, use_container_width=True, hide_index=True)

        # Remove position
        ticker_list = [pos["ticker"] for pos in portfolio]
        col_rm1, col_rm2 = st.columns([2, 1])
        with col_rm1:
            rm_ticker = st.selectbox("Remove position", ticker_list)
        with col_rm2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑 Remove"):
                st.session_state["portfolio"] = [
                    p for p in portfolio if p["ticker"] != rm_ticker
                ]
                st.rerun()

        # Allocation pie chart (2+ positions)
        if len(rows) >= 2:
            st.markdown("**Allocation**")
            labels  = [r["Ticker"] for r in rows]
            values  = [r["_value"]  for r in rows]
            colors  = ["#58a6ff", "#2ea043", "#f85149", "#d29922", "#dda0dd",
                       "#87ceeb", "#98fb98", "#f0e68c", "#ff8c69", "#c9a832"]
            colors  = (colors * 5)[:len(labels)]

            fig_pie = go.Figure(go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=colors),
                showlegend=False,
                textinfo="label+percent",
                textfont=dict(color="#e6edf3", size=12),
            ))
            fig_pie.update_layout(
                height=300,
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                font=dict(color="#8b949e", family="DM Sans"),
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — Signal Scanner
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📋 Signal Scanner")
    st.caption("Scan all watchlist tickers and filter by your signal + risk settings")

    if st.button("🔍 Run Scanner", type="primary"):
        with st.spinner("Scanning all tickers..."):
            results      = []
            all_tickers  = THAI_POPULAR + US_POPULAR
            progress_bar = st.progress(0)

            for i, t in enumerate(all_tickers):
                progress_bar.progress((i + 1) / len(all_tickers))

                df_t = fetch_data(t, "3mo", "1d")
                if df_t is None or len(df_t) < 10:
                    continue

                df_t = compute_indicators(df_t)
                if len(df_t) < 2:
                    continue

                s = compute_signal(df_t, min_conditions)
                if s is None:
                    continue

                last_t = df_t.iloc[-1]
                prev_t = df_t.iloc[-2]

                try:
                    price_t = float(last_t["Close"])
                    prev_p  = float(prev_t["Close"])
                    chg_t   = (price_t - prev_p) / prev_p * 100 if prev_p != 0 else 0.0
                except Exception:
                    price_t = 0.0
                    chg_t   = 0.0

                currency_t = "THB" if t.endswith(".BK") else "USD"

                # Apply filters
                if s["signal"]     not in signal_filter:  continue
                if s["risk_level"] not in risk_filter:     continue
                if s["strength"]   <  min_strength:        continue

                rsi_display = "-"
                if pd.notna(last_t["RSI"]):
                    try:
                        rsi_display = f"{float(last_t['RSI']):.1f}"
                    except Exception:
                        pass

                results.append({
                    "Ticker":   t,
                    "Market":   "🇹🇭 Thai" if t.endswith(".BK") else "🇺🇸 US",
                    "Price":    f"{price_t:,.2f} {currency_t}",
                    "Change %": f"{chg_t:+.2f}%",
                    "Signal":   s["signal"],
                    "Strength": s["strength"],
                    "Risk":     s["risk_level"],
                    "Entry":    f"{s['entry']:,.2f}",
                    "Stop":     f"{s['stop_loss']:,.2f}",
                    "Target":   f"{s['take_profit']:,.2f}",
                    "RSI":      rsi_display,
                })

            progress_bar.empty()

        if not results:
            st.warning(
                "ไม่มี ticker ที่ผ่าน filter ที่ตั้งไว้ — ลองปรับ filter ใน sidebar"
            )
        else:
            st.success(f"พบ {len(results)} ticker ที่ผ่าน filter")

            df_scan = pd.DataFrame(results)

            def style_signal(val):
                if val == "LONG":   return "color: #2ea043; font-weight: bold"
                if val == "SHORT":  return "color: #f85149; font-weight: bold"
                return "color: #8b949e"

            def style_risk(val):
                if val == "HIGH":   return "color: #f85149"
                if val == "MEDIUM": return "color: #f0a500"
                return "color: #2ea043"

            def style_change(val):
                return "color: #2ea043" if "+" in str(val) else "color: #f85149"

            styled = (
                df_scan.style
                .map(style_signal, subset=["Signal"])
                .map(style_risk,   subset=["Risk"])
                .map(style_change, subset=["Change %"])
            )

            st.dataframe(styled, use_container_width=True, hide_index=True)

            # Summary counts
            long_count    = sum(1 for r in results if r["Signal"] == "LONG")
            short_count   = sum(1 for r in results if r["Signal"] == "SHORT")
            neutral_count = sum(1 for r in results if r["Signal"] == "NEUTRAL")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="value" style="color:#2ea043;">{long_count}</div>
                    <div class="label">LONG signals</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="value" style="color:#8b949e;">{neutral_count}</div>
                    <div class="label">NEUTRAL signals</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="value" style="color:#f85149;">{short_count}</div>
                    <div class="label">SHORT signals</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("👆 Click **Run Scanner** to scan all 20 watchlist tickers against your current filter settings.")

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — Divergence Scanner
# ═════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 🔀 Divergence Scanner")

    # Settings summary row
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1: st.metric("Divergence Types",  len(div_types))
    with col_s2: st.metric("Max Bars Ago",       max_bars_ago)
    with col_s3: st.metric("Min Confidence",     f"{min_div_confidence}%")
    with col_s4: st.metric("Pivot Window",        pivot_window)

    # Explainer cards
    st.markdown("""
    <div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin:16px 0'>
      <div style='background:#0d2818;border:1px solid #2ea04366;border-radius:8px;padding:12px'>
        <div style='color:#2ea043;font-weight:700;font-size:0.85rem'>🔄 Regular Bullish</div>
        <div style='color:#8b949e;font-size:0.78rem;margin-top:4px'>
          Price Lower Low + RSI Higher Low &rarr; Reversal up signal
        </div>
      </div>
      <div style='background:#0d2818;border:1px solid #2ea04333;border-radius:8px;padding:12px'>
        <div style='color:#98fb98;font-weight:700;font-size:0.85rem'>↗️ Hidden Bullish</div>
        <div style='color:#8b949e;font-size:0.78rem;margin-top:4px'>
          Price Higher Low + RSI Lower Low &rarr; Uptrend continuation
        </div>
      </div>
      <div style='background:#2d0f0f;border:1px solid #f8514966;border-radius:8px;padding:12px'>
        <div style='color:#f85149;font-weight:700;font-size:0.85rem'>🔄 Regular Bearish</div>
        <div style='color:#8b949e;font-size:0.78rem;margin-top:4px'>
          Price Higher High + RSI Lower High &rarr; Reversal down signal
        </div>
      </div>
      <div style='background:#2d0f0f;border:1px solid #f8514933;border-radius:8px;padding:12px'>
        <div style='color:#ff8c69;font-weight:700;font-size:0.85rem'>↘️ Hidden Bearish</div>
        <div style='color:#8b949e;font-size:0.78rem;margin-top:4px'>
          Price Lower High + RSI Higher High &rarr; Downtrend continuation
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 Scan for Divergences", type="primary", key="div_scan_btn"):
        with st.spinner("Detecting divergence patterns across all tickers..."):
            all_tickers_div = THAI_POPULAR + US_POPULAR
            div_results     = []
            prog_div        = st.progress(0)

            for i, t in enumerate(all_tickers_div):
                prog_div.progress((i + 1) / len(all_tickers_div))

                df_t = fetch_data(t, div_scan_period, "1d")
                if df_t is None or len(df_t) < 30:
                    continue
                df_t = compute_indicators(df_t)
                divs_t = detect_divergences(
                    df_t,
                    lookback_bars=max_bars_ago,
                    pivot_window=pivot_window,
                )

                # Apply filters
                filtered = [
                    d for d in divs_t
                    if d["bars_ago"]   <= max_bars_ago
                    and d["type"]      in div_types
                    and d["confidence"] >= min_div_confidence
                ]
                if not filtered:
                    continue

                # Take the strongest (highest conf, then most recent) per ticker
                best = sorted(filtered,
                              key=lambda x: (-x["confidence"], x["bars_ago"]))[0]

                last_t = df_t.iloc[-1]
                prev_t = df_t.iloc[-2]
                try:
                    price_t = float(last_t["Close"])
                    chg_t   = (price_t - float(prev_t["Close"])) / float(prev_t["Close"]) * 100
                except Exception:
                    price_t, chg_t = 0.0, 0.0

                rsi_t      = float(last_t["RSI"]) if pd.notna(last_t["RSI"]) else 0.0
                currency_t = "THB" if t.endswith(".BK") else "USD"

                try:
                    sig_date_str = best["date"].strftime("%Y-%m-%d")
                except Exception:
                    sig_date_str = str(best["date"])[:10]

                div_results.append({
                    "Ticker":      t,
                    "Market":      "🇹🇭" if t.endswith(".BK") else "🇺🇸",
                    "Price":       f"{price_t:,.2f} {currency_t}",
                    "Chg %":       f"{chg_t:+.2f}%",
                    "Signal Type": best["type"],
                    "Class":       "🔄 Regular" if best["div_class"] == "regular" else "↗️ Hidden",
                    "Direction":   "🟢 Bullish" if best["subtype"] == "bullish" else "🔴 Bearish",
                    "Confidence":  best["confidence"],
                    "Bars Ago":    best["bars_ago"],
                    "Signal Date": sig_date_str,
                    "RSI Now":     f"{rsi_t:.1f}",
                    "Description": best["description"],
                    "_subtype":    best["subtype"],
                })

            prog_div.empty()

        if not div_results:
            st.warning(
                "ไม่พบ divergence ที่ผ่าน filter — "
                "ลองเพิ่ม 'Max Bars Ago' หรือลด 'Min Confidence'"
            )
        else:
            # Sort: bullish first, then by confidence descending
            div_results.sort(key=lambda x: (x["_subtype"] != "bullish", -x["Confidence"]))

            bull_res = [r for r in div_results if r["_subtype"] == "bullish"]
            bear_res = [r for r in div_results if r["_subtype"] == "bearish"]

            st.success(
                f"พบ {len(div_results)} ticker &nbsp;·&nbsp; "
                f"🟢 Bullish: {len(bull_res)} &nbsp;·&nbsp; "
                f"🔴 Bearish: {len(bear_res)}"
            )

            # Summary metric cards
            mc1, mc2, mc3, mc4 = st.columns(4)
            reg_bull = sum(1 for r in div_results if "Regular Bullish" in r["Signal Type"])
            hid_bull = sum(1 for r in div_results if "Hidden Bullish"  in r["Signal Type"])
            reg_bear = sum(1 for r in div_results if "Regular Bearish" in r["Signal Type"])
            avg_conf = sum(r["Confidence"] for r in div_results) / len(div_results)

            with mc1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='value' style='color:#2ea043'>{reg_bull}</div>
                    <div class='label'>Regular Bullish</div>
                </div>""", unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='value' style='color:#98fb98'>{hid_bull}</div>
                    <div class='label'>Hidden Bullish</div>
                </div>""", unsafe_allow_html=True)
            with mc3:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='value' style='color:#f85149'>{reg_bear}</div>
                    <div class='label'>Regular Bearish</div>
                </div>""", unsafe_allow_html=True)
            with mc4:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='value' style='color:#f0a500'>{avg_conf:.0f}%</div>
                    <div class='label'>Avg Confidence</div>
                </div>""", unsafe_allow_html=True)

            # Results table
            display_cols = [c for c in div_results[0].keys() if not c.startswith("_")]
            df_div = pd.DataFrame(div_results)[display_cols]

            def style_direction(val):
                if "Bullish" in str(val): return "color:#2ea043;font-weight:bold"
                if "Bearish" in str(val): return "color:#f85149;font-weight:bold"
                return ""

            def style_conf(val):
                if val >= 85: return "color:#2ea043;font-weight:bold"
                if val >= 75: return "color:#f0a500"
                return "color:#8b949e"

            def style_bars(val):
                if val <= 3:  return "color:#2ea043;font-weight:bold"
                if val <= 7:  return "color:#f0a500"
                return "color:#8b949e"

            styled_div = (
                df_div.style
                .map(style_direction, subset=["Direction"])
                .map(style_conf,      subset=["Confidence"])
                .map(style_bars,      subset=["Bars Ago"])
            )
            st.dataframe(styled_div, use_container_width=True, hide_index=True)

            # Detail expanders
            st.markdown("**📋 Divergence Details**")
            for r in div_results[:10]:
                color = "#2ea043" if r["_subtype"] == "bullish" else "#f85149"
                with st.expander(
                    f"{r['Ticker']} — {r['Signal Type']} · "
                    f"{r['Bars Ago']} bars ago · {r['Confidence']}% conf"
                ):
                    ec1, ec2, ec3 = st.columns(3)
                    with ec1:
                        st.markdown(f"**Ticker:** {r['Ticker']}")
                        st.markdown(f"**Price:** {r['Price']} ({r['Chg %']})")
                        st.markdown(f"**RSI now:** {r['RSI Now']}")
                    with ec2:
                        st.markdown(f"**Signal date:** {r['Signal Date']}")
                        st.markdown(f"**Bars ago:** {r['Bars Ago']}")
                        st.markdown(f"**Confidence:** {r['Confidence']}%")
                    with ec3:
                        st.markdown(f"**Type:** {r['Signal Type']}")
                        st.markdown(f"**Class:** {r['Class']}")
                    st.markdown(f"**📖 Explanation:** {r['Description']}")
                    if st.button(
                        f"📊 View chart for {r['Ticker']}",
                        key=f"view_div_{r['Ticker']}",
                    ):
                        st.info(
                            f"ไปที่ Sidebar → เลือก Market: Manual → พิมพ์ {r['Ticker']}"
                        )
    else:
        st.info(
            "👆 Click **Scan for Divergences** to search all 20 watchlist tickers "
            "for RSI divergence patterns based on your sidebar settings."
        )

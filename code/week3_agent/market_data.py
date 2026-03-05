"""
Market data helpers — yfinance for prices, finnhub for news & earnings.
"""

from __future__ import annotations

import datetime as dt
import os

import finnhub
import yfinance as yf


def get_finnhub_client() -> finnhub.Client:
    key = os.environ.get("FINNHUB_API_KEY", "")
    if not key:
        raise RuntimeError(
            "FINNHUB_API_KEY not set. "
            "Get a free key at https://finnhub.io and export it."
        )
    return finnhub.Client(api_key=key)


# ── prices ────────────────────────────────────────────────────

def get_price_history(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
) -> list[dict]:
    """Fetch OHLCV data via yfinance. Returns list of row dicts."""
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        return []
    # yfinance may return MultiIndex columns when single ticker
    if hasattr(df.columns, "droplevel"):
        try:
            df.columns = df.columns.droplevel(1)
        except Exception:
            pass
    df = df.reset_index()
    rows = []
    for _, r in df.iterrows():
        rows.append(
            {
                "date": str(r["Date"].date()) if hasattr(r["Date"], "date") else str(r["Date"]),
                "open": round(float(r["Open"]), 2),
                "high": round(float(r["High"]), 2),
                "low": round(float(r["Low"]), 2),
                "close": round(float(r["Close"]), 2),
                "volume": int(r["Volume"]),
            }
        )
    return rows


def get_latest_price(ticker: str) -> float:
    """Get the most recent closing price for *ticker*."""
    hist = get_price_history(ticker, period="5d", interval="1d")
    if not hist:
        raise ValueError(f"No price data for {ticker}")
    return hist[-1]["close"]


# ── news ──────────────────────────────────────────────────────

def get_news_headlines(
    ticker: str,
    days_back: int = 7,
) -> list[dict]:
    """Fetch recent company news from finnhub."""
    client = get_finnhub_client()
    today = dt.date.today()
    from_date = (today - dt.timedelta(days=days_back)).isoformat()
    to_date = today.isoformat()
    raw = client.company_news(ticker, _from=from_date, to=to_date)
    results = []
    for item in raw[:20]:  # cap at 20 headlines
        results.append(
            {
                "datetime": dt.datetime.fromtimestamp(item["datetime"]).isoformat(
                    timespec="seconds"
                ),
                "headline": item.get("headline", ""),
                "summary": item.get("summary", "")[:300],
                "source": item.get("source", ""),
                "url": item.get("url", ""),
            }
        )
    return results


# ── earnings ──────────────────────────────────────────────────

def get_earnings_calendar(
    ticker: str,
) -> list[dict]:
    """Fetch upcoming earnings dates from finnhub."""
    client = get_finnhub_client()
    today = dt.date.today()
    from_date = today.isoformat()
    to_date = (today + dt.timedelta(days=90)).isoformat()
    raw = client.earnings_calendar(
        _from=from_date, to=to_date, symbol=ticker
    )
    results = []
    for item in raw.get("earningsCalendar", []):
        results.append(
            {
                "date": item.get("date", ""),
                "ticker": item.get("symbol", ticker),
                "eps_estimate": item.get("epsEstimate"),
                "revenue_estimate": item.get("revenueEstimate"),
            }
        )
    return results

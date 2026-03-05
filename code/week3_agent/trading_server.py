"""
MCP Trading Server — exposes trading tools to Claude Code.

Run with:  python trading_server.py
Register:  claude mcp add --transport stdio --scope user \
             --env FINNHUB_API_KEY=<your_key> \
             trading-agent -- python /absolute/path/to/trading_server.py
"""

from __future__ import annotations

import json
from mcp.server.fastmcp import FastMCP

from paper_trading import Portfolio
from market_data import (
    get_price_history as _get_price_history,
    get_latest_price,
    get_news_headlines as _get_news_headlines,
    get_earnings_calendar as _get_earnings_calendar,
)
from sentiment import analyze_sentiment as _analyze_sentiment
from indicators import compute_indicators as _compute_indicators
from backtest import backtest_strategy as _backtest_strategy

# ── state ─────────────────────────────────────────────────────
portfolio = Portfolio()
mcp = FastMCP("trading-agent")


# ── market data tools ─────────────────────────────────────────

@mcp.tool()
async def get_price_history(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
) -> str:
    """Fetch historical OHLCV price data for a stock.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL", "MSFT").
        period: How far back to fetch. One of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max.
        interval: Bar size. One of: 1m, 5m, 15m, 1h, 1d, 1wk, 1mo.

    Returns:
        JSON array of {date, open, high, low, close, volume} objects.
    """
    rows = _get_price_history(ticker, period=period, interval=interval)
    return json.dumps(rows[-60:], indent=2)  # cap to last 60 bars


@mcp.tool()
async def get_news_headlines(ticker: str, days_back: int = 7) -> str:
    """Fetch recent news headlines for a stock from Finnhub.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL").
        days_back: Number of days to look back (default 7).

    Returns:
        JSON array of {datetime, headline, summary, source, url} objects.
    """
    headlines = _get_news_headlines(ticker, days_back=days_back)
    return json.dumps(headlines, indent=2)


@mcp.tool()
async def get_earnings_calendar(ticker: str) -> str:
    """Fetch upcoming earnings dates for a stock from Finnhub.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL").

    Returns:
        JSON array of {date, ticker, eps_estimate, revenue_estimate} objects.
    """
    cal = _get_earnings_calendar(ticker)
    return json.dumps(cal, indent=2)


# ── analysis tools ────────────────────────────────────────────

@mcp.tool()
async def analyze_sentiment(headlines: list[str]) -> str:
    """Run FinBERT sentiment analysis on a list of financial texts.

    Use this after fetching news headlines to score them as
    positive, negative, or neutral.

    Args:
        headlines: List of headline strings to analyze.

    Returns:
        JSON array of {text, label, score} objects.
    """
    results = _analyze_sentiment(headlines)
    return json.dumps(results, indent=2)


@mcp.tool()
async def compute_indicators(ticker: str, period: str = "6mo") -> str:
    """Compute technical indicators (RSI, MACD, Bollinger Bands, SMAs) for a stock.

    Args:
        ticker: Stock ticker symbol.
        period: How far back to fetch price data (default "6mo").

    Returns:
        JSON object with latest indicator values:
        {close, rsi_14, macd, macd_signal, macd_histogram,
         bollinger_upper, bollinger_middle, bollinger_lower,
         sma_20, sma_50}.
    """
    rows = _get_price_history(ticker, period=period)
    indicators = _compute_indicators(rows)
    return json.dumps(indicators, indent=2)


# ── trading tools ─────────────────────────────────────────────

@mcp.tool()
async def place_order(ticker: str, side: str, quantity: int) -> str:
    """Place a market order (paper trading — no real money).

    Executes immediately at the current market price.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL").
        side: "buy" or "sell".
        quantity: Number of shares to trade (must be positive).

    Returns:
        JSON fill confirmation with {timestamp, ticker, side, quantity,
        price, notional}.
    """
    price = get_latest_price(ticker)
    fill = portfolio.place_order(ticker, side, quantity, price)
    return json.dumps(
        {
            "status": "filled",
            "timestamp": fill.timestamp,
            "ticker": fill.ticker,
            "side": fill.side,
            "quantity": fill.quantity,
            "price": fill.price,
            "notional": fill.notional,
        },
        indent=2,
    )


@mcp.tool()
async def get_portfolio() -> str:
    """Get current portfolio snapshot: positions, cash, PnL, NAV.

    Returns:
        JSON object with {cash, positions, total_market_value,
        total_unrealised_pnl, nav, total_return_pct, num_trades}.
    """
    # fetch current prices for all held tickers
    current_prices = {}
    for ticker in portfolio.positions:
        try:
            current_prices[ticker] = get_latest_price(ticker)
        except Exception:
            pass
    summary = portfolio.get_portfolio_summary(current_prices)
    return json.dumps(summary, indent=2)


@mcp.tool()
async def get_pnl() -> str:
    """Get profit & loss summary and full trade history.

    Returns:
        JSON object with {portfolio_summary, trade_history}.
    """
    current_prices = {}
    for ticker in portfolio.positions:
        try:
            current_prices[ticker] = get_latest_price(ticker)
        except Exception:
            pass
    summary = portfolio.get_portfolio_summary(current_prices)
    history = portfolio.get_order_history()
    return json.dumps(
        {"portfolio_summary": summary, "trade_history": history},
        indent=2,
    )


# ── backtesting tools ────────────────────────────────────────

@mcp.tool()
async def backtest_sentiment_strategy(
    ticker: str,
    period: str = "1y",
    long_threshold: float = 0.2,
    short_threshold: float = -0.2,
) -> str:
    """Backtest a sentiment-based trading strategy on historical data.

    Generates a synthetic sentiment signal correlated with returns,
    then runs a long/short backtest.

    Args:
        ticker: Stock ticker symbol.
        period: Historical period to backtest over (default "1y").
        long_threshold: Go long when signal > this (default 0.2).
        short_threshold: Go short when signal < this (default -0.2).

    Returns:
        JSON object with {total_return_pct, annualised_sharpe,
        max_drawdown_pct, num_trades, final_equity}.
    """
    import random
    import math

    rows = _get_price_history(ticker, period=period)
    if len(rows) < 30:
        return json.dumps({"error": f"Not enough data for {ticker}"})

    # generate synthetic signal correlated with next-day returns
    random.seed(42)
    returns = [0.0] + [
        (rows[i]["close"] - rows[i - 1]["close"]) / rows[i - 1]["close"]
        for i in range(1, len(rows))
    ]
    signal = []
    for r in returns:
        noise = random.gauss(0, 0.5)
        sig = 0.3 * r * 100 + noise  # weak correlation with returns
        sig = max(-1.0, min(1.0, sig))
        signal.append(round(sig, 4))

    result = _backtest_strategy(
        rows, signal,
        long_threshold=long_threshold,
        short_threshold=short_threshold,
    )
    return json.dumps(result, indent=2)


# ── entry point ───────────────────────────────────────────────

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

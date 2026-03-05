"""
Technical indicators — computed from OHLCV data.

All functions accept a list[dict] with at least a "close" key
(the format returned by market_data.get_price_history).
"""

from __future__ import annotations


def _closes(rows: list[dict]) -> list[float]:
    return [r["close"] for r in rows]


def sma(rows: list[dict], window: int = 20) -> list[dict]:
    """Simple Moving Average."""
    closes = _closes(rows)
    result = []
    for i in range(len(closes)):
        if i < window - 1:
            result.append({"date": rows[i]["date"], "sma": None})
        else:
            avg = sum(closes[i - window + 1 : i + 1]) / window
            result.append({"date": rows[i]["date"], "sma": round(avg, 2)})
    return result


def ema(closes: list[float], window: int) -> list[float]:
    """Exponential Moving Average (internal helper)."""
    k = 2 / (window + 1)
    vals = [closes[0]]
    for c in closes[1:]:
        vals.append(c * k + vals[-1] * (1 - k))
    return vals


def rsi(rows: list[dict], window: int = 14) -> list[dict]:
    """Relative Strength Index."""
    closes = _closes(rows)
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    result = [{"date": rows[0]["date"], "rsi": None}]

    gains, losses = [], []
    for i, d in enumerate(deltas):
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
        if i < window - 1:
            result.append({"date": rows[i + 1]["date"], "rsi": None})
        elif i == window - 1:
            avg_gain = sum(gains[-window:]) / window
            avg_loss = sum(losses[-window:]) / window
            rs = avg_gain / avg_loss if avg_loss != 0 else 100
            result.append({"date": rows[i + 1]["date"], "rsi": round(100 - 100 / (1 + rs), 2)})
        else:
            avg_gain = (avg_gain * (window - 1) + gains[-1]) / window
            avg_loss = (avg_loss * (window - 1) + losses[-1]) / window
            rs = avg_gain / avg_loss if avg_loss != 0 else 100
            result.append({"date": rows[i + 1]["date"], "rsi": round(100 - 100 / (1 + rs), 2)})
    return result


def macd(
    rows: list[dict],
    fast: int = 12,
    slow: int = 26,
    signal_window: int = 9,
) -> list[dict]:
    """MACD line, signal line, and histogram."""
    closes = _closes(rows)
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    macd_line = [round(f - s, 4) for f, s in zip(ema_fast, ema_slow)]
    signal_line = ema(macd_line, signal_window)
    result = []
    for i in range(len(rows)):
        result.append(
            {
                "date": rows[i]["date"],
                "macd": round(macd_line[i], 4),
                "signal": round(signal_line[i], 4),
                "histogram": round(macd_line[i] - signal_line[i], 4),
            }
        )
    return result


def bollinger_bands(
    rows: list[dict], window: int = 20, num_std: float = 2.0
) -> list[dict]:
    """Bollinger Bands (middle, upper, lower)."""
    closes = _closes(rows)
    result = []
    for i in range(len(closes)):
        if i < window - 1:
            result.append(
                {"date": rows[i]["date"], "upper": None, "middle": None, "lower": None}
            )
        else:
            window_slice = closes[i - window + 1 : i + 1]
            mid = sum(window_slice) / window
            variance = sum((x - mid) ** 2 for x in window_slice) / window
            std = variance**0.5
            result.append(
                {
                    "date": rows[i]["date"],
                    "upper": round(mid + num_std * std, 2),
                    "middle": round(mid, 2),
                    "lower": round(mid - num_std * std, 2),
                }
            )
    return result


def compute_indicators(rows: list[dict]) -> dict:
    """Compute all indicators and return the most recent values."""
    if len(rows) < 26:
        return {"error": "Need at least 26 data points"}

    rsi_vals = rsi(rows)
    macd_vals = macd(rows)
    bb_vals = bollinger_bands(rows)
    sma_20 = sma(rows, 20)
    sma_50 = sma(rows, 50)

    latest = rows[-1]
    return {
        "date": latest["date"],
        "close": latest["close"],
        "rsi_14": rsi_vals[-1]["rsi"],
        "macd": macd_vals[-1]["macd"],
        "macd_signal": macd_vals[-1]["signal"],
        "macd_histogram": macd_vals[-1]["histogram"],
        "bollinger_upper": bb_vals[-1]["upper"],
        "bollinger_middle": bb_vals[-1]["middle"],
        "bollinger_lower": bb_vals[-1]["lower"],
        "sma_20": sma_20[-1]["sma"],
        "sma_50": sma_50[-1]["sma"] if len(rows) >= 50 else None,
    }

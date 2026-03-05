"""
Simple backtesting engine for signal-based strategies.

Given a price series and a signal series, simulates a long/short strategy
and reports performance metrics.
"""

from __future__ import annotations

import math


def backtest_strategy(
    rows: list[dict],
    signal: list[float],
    long_threshold: float = 0.2,
    short_threshold: float = -0.2,
    initial_cash: float = 100_000.0,
) -> dict:
    """
    Backtest a strategy driven by a signal in [-1, 1].

    Parameters
    ----------
    rows : list[dict]
        Price history from get_price_history (must have "date" and "close").
    signal : list[float]
        Signal values aligned with *rows*. +1 = max long, -1 = max short.
    long_threshold : float
        Go long when signal > this.
    short_threshold : float
        Go short when signal < this.
    initial_cash : float
        Starting capital.

    Returns
    -------
    dict with equity_curve, sharpe, total_return, max_drawdown, num_trades.
    """
    if len(rows) != len(signal):
        raise ValueError(
            f"rows ({len(rows)}) and signal ({len(signal)}) must be same length"
        )

    cash = initial_cash
    position = 0.0       # shares held (negative = short)
    equity_curve = []
    daily_returns = []
    num_trades = 0

    for i, (row, sig) in enumerate(zip(rows, signal)):
        price = row["close"]

        # determine target position
        if sig > long_threshold:
            target = 1     # fully long
        elif sig < short_threshold:
            target = -1    # fully short
        else:
            target = 0     # flat

        # target shares (invest 100% of initial capital)
        target_shares = target * (initial_cash / price)

        # rebalance if target changed
        delta = target_shares - position
        if abs(delta) > 0.01:
            cash -= delta * price
            position = target_shares
            num_trades += 1

        # mark to market
        equity = cash + position * price
        equity_curve.append(
            {"date": row["date"], "equity": round(equity, 2)}
        )
        if i > 0:
            prev_eq = equity_curve[i - 1]["equity"]
            daily_returns.append((equity - prev_eq) / prev_eq if prev_eq != 0 else 0)

    # ── metrics ───────────────────────────────────────────────
    total_return = (equity_curve[-1]["equity"] / initial_cash - 1) * 100

    # annualised sharpe (252 trading days)
    if daily_returns:
        mean_r = sum(daily_returns) / len(daily_returns)
        var_r = sum((r - mean_r) ** 2 for r in daily_returns) / len(daily_returns)
        std_r = math.sqrt(var_r) if var_r > 0 else 1e-9
        sharpe = (mean_r / std_r) * math.sqrt(252)
    else:
        sharpe = 0.0

    # max drawdown
    peak = equity_curve[0]["equity"]
    max_dd = 0.0
    for pt in equity_curve:
        if pt["equity"] > peak:
            peak = pt["equity"]
        dd = (peak - pt["equity"]) / peak
        if dd > max_dd:
            max_dd = dd

    return {
        "total_return_pct": round(total_return, 2),
        "annualised_sharpe": round(sharpe, 2),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "num_trades": num_trades,
        "final_equity": equity_curve[-1]["equity"],
        "equity_curve_first_5": equity_curve[:5],
        "equity_curve_last_5": equity_curve[-5:],
    }

"""
Paper trading engine — in-memory portfolio management.

Tracks positions, cash, orders, and computes PnL.
All state lives in memory (resets when the server restarts).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field


@dataclass
class Fill:
    timestamp: str
    ticker: str
    side: str          # "buy" or "sell"
    quantity: float
    price: float
    notional: float


@dataclass
class Portfolio:
    cash: float = 100_000.0
    positions: dict[str, float] = field(default_factory=dict)      # ticker -> quantity
    cost_basis: dict[str, float] = field(default_factory=dict)     # ticker -> avg cost per share
    order_history: list[Fill] = field(default_factory=list)

    # ── orders ────────────────────────────────────────────────

    def place_order(
        self,
        ticker: str,
        side: str,
        quantity: float,
        current_price: float,
    ) -> Fill:
        """Execute a market order at *current_price* (instant fill)."""
        side = side.lower()
        if side not in ("buy", "sell"):
            raise ValueError(f"side must be 'buy' or 'sell', got '{side}'")
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        notional = round(quantity * current_price, 2)

        if side == "buy":
            if notional > self.cash:
                raise ValueError(
                    f"Insufficient cash: need ${notional:,.2f}, "
                    f"have ${self.cash:,.2f}"
                )
            self.cash -= notional
            prev_qty = self.positions.get(ticker, 0.0)
            prev_cost = self.cost_basis.get(ticker, 0.0)
            new_qty = prev_qty + quantity
            # weighted average cost basis
            if new_qty > 0:
                self.cost_basis[ticker] = (
                    (prev_cost * prev_qty + current_price * quantity) / new_qty
                )
            self.positions[ticker] = new_qty
        else:  # sell
            held = self.positions.get(ticker, 0.0)
            if quantity > held:
                raise ValueError(
                    f"Cannot sell {quantity} shares of {ticker}: "
                    f"only hold {held}"
                )
            self.cash += notional
            self.positions[ticker] = held - quantity
            if self.positions[ticker] == 0:
                del self.positions[ticker]
                del self.cost_basis[ticker]

        fill = Fill(
            timestamp=dt.datetime.now().isoformat(timespec="seconds"),
            ticker=ticker,
            side=side,
            quantity=quantity,
            price=current_price,
            notional=notional,
        )
        self.order_history.append(fill)
        return fill

    # ── queries ───────────────────────────────────────────────

    def get_portfolio_summary(
        self, current_prices: dict[str, float]
    ) -> dict:
        """Return portfolio snapshot with market values and PnL."""
        positions_detail = []
        total_market_value = 0.0
        total_unrealised_pnl = 0.0

        for ticker, qty in sorted(self.positions.items()):
            price = current_prices.get(ticker)
            if price is None:
                continue
            market_value = round(qty * price, 2)
            cost = self.cost_basis.get(ticker, 0.0)
            unrealised_pnl = round((price - cost) * qty, 2)
            total_market_value += market_value
            total_unrealised_pnl += unrealised_pnl
            positions_detail.append(
                {
                    "ticker": ticker,
                    "quantity": qty,
                    "avg_cost": round(cost, 2),
                    "current_price": price,
                    "market_value": market_value,
                    "unrealised_pnl": unrealised_pnl,
                }
            )

        nav = round(self.cash + total_market_value, 2)
        return {
            "cash": round(self.cash, 2),
            "positions": positions_detail,
            "total_market_value": round(total_market_value, 2),
            "total_unrealised_pnl": round(total_unrealised_pnl, 2),
            "nav": nav,
            "total_return_pct": round((nav / 100_000 - 1) * 100, 2),
            "num_trades": len(self.order_history),
        }

    def get_order_history(self) -> list[dict]:
        return [
            {
                "timestamp": f.timestamp,
                "ticker": f.ticker,
                "side": f.side,
                "quantity": f.quantity,
                "price": f.price,
                "notional": f.notional,
            }
            for f in self.order_history
        ]

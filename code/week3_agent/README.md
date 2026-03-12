# Tutorial: Build an AI Trading Agent with VS Code Chat (Claude)


> You will build a trading agent that can fetch market data, analyse news
> sentiment, compute technical indicators, and execute paper trades —
> all by talking to it in plain English through VS Code Chat with Claude.
>
> There is no custom UI. VS Code Chat **is** the interface.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  You  ←→  VS Code Chat (Session: Claude)    │
│              │                               │
│              │  MCP protocol (stdio)         │
│              ▼                               │
│  ┌───────────────────────────────────┐       │
│  │  trading_server.py  (MCP server)  │       │
│  │                                   │       │
│  │  Tools:                           │       │
│  │   • get_price_history             │       │
│  │   • get_news_headlines            │       │
│  │   • get_earnings_calendar         │       │
│  │   • analyze_sentiment             │       │
│  │   • compute_indicators            │       │
│  │   • place_order                   │       │
│  │   • get_portfolio                 │       │
│  │   • get_pnl                       │       │
│  │   • backtest_sentiment_strategy   │       │
│  └───────────┬───────────────────────┘       │
│              │                               │
│     ┌────────┼────────┐                      │
│     ▼        ▼        ▼                      │
│  yfinance  finnhub  FinBERT                  │
└─────────────────────────────────────────────┘
```

When you ask Claude "buy 50 shares of AAPL", Claude recognises this requires
the `place_order` tool, calls your MCP server, and your Python code executes
the paper trade. Claude sees the result and reports back. This is the same
**LLM agent loop** from the lecture: perceive → reason → act → observe → repeat.

---

## Part 0 — Setup (15 min)

### 0.1 Set up VS Code Chat with Claude

1. Open **VS Code**
2. Make sure you are on the **latest version of VS Code**
3. Go to **Extensions** (⇧⌘X / Ctrl+Shift+X), search **"Claude Code"**, and install the Claude Code extension
4. Open **VS Code Chat** (⇧⌘I / Ctrl+Shift+I)
5. Set **Session Target** to **Claude**
6. Sign in with your **GitHub account** in VS Code if you have not already (Imperial students should have **GitHub Copilot Pro**, and Claude requests count toward that allowance)

### 0.2 Get a Finnhub API key

1. Go to [https://finnhub.io](https://finnhub.io) and create a free account
2. Copy your API key from the dashboard
3. Keep it handy — you will use it in Step 0.5

### 0.3 Clone and enter the project

Open a terminal in VS Code (`` Ctrl+` ``) and run:

```bash
cd /path/to/gen-ai-imperial/code/week3_agent
```

### 0.4 Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** The first run of `analyze_sentiment` will download the FinBERT
> model (~400 MB). This happens once.

### 0.5 Register the MCP server

This is the key step. You tell Claude in VS Code Chat: "there is a Python server that
exposes trading tools — here is how to run it."

In the VS Code terminal, run (replace the paths and API key):

```bash
claude mcp add `
  --transport stdio `
  --env FINNHUB_API_KEY=crpia01r01qsek0frl20crpia01r01qsek0frl2g `
  --scope user `
  trading-agent `
  -- "C:\Users\chris\Anaconda\envs\math70065\python.exe" `
     "C:\Users\chris\VSCodeProjects\gen-ai-imperial\code\week3_agent\trading_server.py"
```

> **What this does:** Registers an MCP server named `trading-agent` that
> Claude will launch as a subprocess. Claude can now discover and call
> all 9 tools defined in `trading_server.py`.

Verify it worked:

```bash
claude mcp list
```

You should see `trading-agent` in the output. Now **restart VS Code Chat**
in VS Code (close and reopen Chat, or reload the window with ⇧⌘P →
"Developer: Reload Window").

### 0.6 Smoke test

In VS Code Chat (with Session Target set to Claude), type:

```
What tools do you have available from the trading-agent server?
```

Claude should list all 9 tools. If it does — you are ready.

---

## Part 1 — Market Data (15 min)

Now you will interact with your trading agent. Everything below happens in
VS Code Chat inside VS Code.

### Exercise 1.1 — Fetch price history

Type:

```
Get me the last 3 months of daily price data for AAPL
```

Claude will call `get_price_history(ticker="AAPL", period="3mo")` and show
you the OHLCV data.

**Observe:** Claude received raw JSON from your MCP server and presented it
in a readable way. You did not write any formatting code — the LLM handles
presentation.

### Exercise 1.2 — Compare two stocks

```
Compare the 6-month price performance of NVDA vs MSFT.
Which one had higher volatility?
```

Claude will call `get_price_history` twice (once per ticker), then reason
over the data to answer your question.

**Key insight:** The agent calls tools *and* reasons over the results. This
is the "perceive → reason" loop from the lecture.

### Exercise 1.3 — Fetch news

```
What are the latest news headlines for TSLA?
```

Claude calls `get_news_headlines(ticker="TSLA")` via Finnhub and presents
the results.

### Exercise 1.4 — Earnings calendar

```
When is AAPL's next earnings date?
```

---

## Part 2 — Sentiment Analysis (15 min)

### Exercise 2.1 — Analyse news sentiment

```
Fetch the latest news for NVDA and run sentiment analysis on the headlines.
Summarise the overall sentiment.
```

**What happens under the hood:**
1. Claude calls `get_news_headlines(ticker="NVDA")`
2. Claude extracts the headline strings from the result
3. Claude calls `analyze_sentiment(headlines=[...])` — this runs FinBERT
4. Claude aggregates the scores and presents a summary

This is a **multi-step tool-use chain** — the agent planned and executed
two sequential tool calls without you specifying the intermediate steps.

### Exercise 2.2 — Sentiment-driven analysis

```
Fetch news for JPM, GS, and MS. Run sentiment analysis on all of them.
Which bank has the most positive news sentiment right now?
```

Claude will make 3 news calls + 3 sentiment calls, then compare.

### Exercise 2.3 — Connect to the lecture

Recall from the lecture: **Lopez-Lira & Tang (2023)** showed GPT-4 headline
sentiment predicts next-day cross-sectional returns, with the effect
strongest for small caps and after negative news.

Ask Claude:

```
Based on the sentiment analysis you just did, which bank would you
overweight and which would you underweight? Explain your reasoning
in terms of the sentiment signal strength.
```

---

## Part 3 — Technical Analysis (10 min)

### Exercise 3.1 — Compute indicators

```
Compute technical indicators for AAPL. Is it overbought or oversold
based on RSI and Bollinger Bands?
```

Claude calls `compute_indicators(ticker="AAPL")` and interprets the
output — RSI > 70 means overbought, < 30 means oversold; price near
upper Bollinger Band suggests overbought.

### Exercise 3.2 — Multi-signal view

```
Give me a full technical analysis of TSLA: RSI, MACD, Bollinger Bands,
and moving averages. What is the overall technical outlook?
```

---

## Part 4 — Paper Trading (20 min)

### Exercise 4.1 — Place your first trade

```
Buy 100 shares of AAPL
```

Claude calls `place_order(ticker="AAPL", side="buy", quantity=100)`.
You will see the fill confirmation with price and notional value.

### Exercise 4.2 — Build a position

```
Also buy 50 shares of MSFT and 200 shares of NVDA
```

### Exercise 4.3 — Check your portfolio

```
Show me my current portfolio
```

Claude calls `get_portfolio()` and shows you positions, market values,
unrealised PnL, and total NAV.

### Exercise 4.4 — The agent as trader

Now give Claude a complex instruction:

```
I want you to act as my trading agent. Analyse TSLA using both
sentiment (fetch and analyse news) and technical indicators.
Based on your analysis, decide whether to buy, sell, or hold.
If you decide to trade, execute the order. Explain your reasoning.
```

**This is the full agent loop:**
1. **Perceive** — fetch news + price data + indicators
2. **Reason** — synthesise sentiment and technicals into a view
3. **Act** — place an order (or decide to hold)
4. **Observe** — confirm the fill and updated portfolio

This single prompt triggers 3-5 tool calls. Watch Claude's chain of thought.

### Exercise 4.5 — Portfolio review

```
Review my full portfolio. For each position, fetch the latest news
and indicators. Give me a risk assessment and suggest any trades
to improve the portfolio.
```

### Exercise 4.6 — Close a position

```
Sell all my AAPL shares
```

Then check PnL:

```
Show me my full trade history and P&L
```

---

## Part 5 — Backtesting (10 min)

### Exercise 5.1 — Run a backtest

```
Backtest a sentiment-based strategy on AAPL over the last year.
Report the Sharpe ratio, total return, and max drawdown.
```

Claude calls `backtest_sentiment_strategy(ticker="AAPL", period="1y")`.

### Exercise 5.2 — Compare tickers

```
Backtest the sentiment strategy on AAPL, MSFT, NVDA, and TSLA.
Which stock would this strategy have performed best on?
```

### Exercise 5.3 — Tune thresholds

```
Run the AAPL backtest again, but try different threshold values:
(0.1, -0.1), (0.3, -0.3), and (0.5, -0.5).
Which thresholds give the best risk-adjusted returns?
```

---

## Part 6 — Putting It All Together (5 min)

### Exercise 6.1 — The full agent

Give Claude a high-level mandate and let it operate autonomously:

```
You are a quantitative trading agent. Your mandate:
- Universe: AAPL, MSFT, GOOGL, AMZN, NVDA
- Strategy: For each stock, combine sentiment and technical signals
  to decide position sizing
- Constraints: Start with $100K cash, invest in at most 3 stocks
- Goal: Maximise risk-adjusted returns

Analyse all 5 stocks, select your top 3, size positions, and execute.
Show your reasoning at each step.
```

Watch how Claude orchestrates 15+ tool calls to build a portfolio
from scratch.

---

## Recap — What You Built

| Component | Role | Lecture concept |
|-----------|------|-----------------|
| `trading_server.py` | MCP server exposing tools | **Tool use** — the agent's interface to the world |
| `market_data.py` | Price data + news feed | **Information gap** — unstructured text at scale |
| `sentiment.py` | FinBERT sentiment scoring | **Sentiment analysis** layer 3 (contextualised models) |
| `indicators.py` | RSI, MACD, Bollinger | Classical quant signals the agent reasons over |
| `paper_trading.py` | Portfolio + order execution | The "act" step in the agent loop |
| `backtest.py` | Historical strategy testing | Statistical validation before deployment |
| Claude (in VS Code Chat) | The LLM agent (planning + reasoning) | **LLM Agent** = tool use + planning + memory |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No tools found" | Restart VS Code Chat after `claude mcp add`. Check `claude mcp list`. |
| "FINNHUB_API_KEY not set" | Re-run `claude mcp add` with `--env FINNHUB_API_KEY=your_key`. |
| Slow first sentiment call | FinBERT download (~400 MB) on first use. Subsequent calls are fast. |
| "Insufficient cash" | Your paper portfolio started with $100K. Check `get_portfolio`. |
| Rate limit on free tier | Wait a moment and retry. Each exercise is designed to be self-contained. |
| yfinance returns empty | Check the ticker symbol. Some tickers require exchange suffix (e.g. "HSBA.L"). |

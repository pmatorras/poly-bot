# PolyBot: Automated Polymarket Arbitrage & Paper Trading

[![PolyBot Daily Pipeline](https://github.com/pmatorras/poly-bot/actions/workflows/polybot.yml/badge.svg)](https://github.com/pmatorras/poly-bot/actions/workflows/polybot.yml)

PolyBot is an automated **paper-trading** bot that identifies potential arbitrage opportunities and positive Expected Value (+EV) edges between traditional sportsbooks and Polymarket's decentralized order books. 

Currently tracking **NBA**, **NHL**, and **NCAA Basketball**.

## How It Works

The bot runs on an automated daily schedule via GitHub Actions, executing the following pipeline:

1. **Odds Fetching:** Pulls live, normalized sportsbook odds using [The Odds API](https://the-odds-api.com/).
2. **Name Normalization:** Automatically standardizes and maps NCAA college team names to match Polymarket's dynamic abbreviation slugs.
3. **Edge Calculation:** Scrapes Polymarket order books, comparing traditional market implied probabilities against current Polymarket `ask` prices to find actionable edges.
4. **Paper Trading:** Calculates optimal theoretical bet sizes using Quarter-Kelly Criterion based on available liquidity and bankroll.
5. **Grading:** Checks real-world match outcomes from the previous day and updates the running PnL in the tracking database.

All historical mock trades and current pending positions are automatically committed and stored in [`data/paper_trades.csv`](./data/paper_trades.csv).

## Local Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/pmatorras/poly-bot.git
    cd poly-bot
    ```

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

1. Set your Odds API Key as an environment variable:

    ```bash
    export ODDS_API_KEY="your_api_key_here"
    ```

1. Run the full pipeline manually:

    ```bash
    PYTHONPATH=. python src/poly_bot/main.py --run pipeline
    ```

## Automation

The pipeline is fully automated via GitHub Actions (`.github/workflows/polybot.yml`), triggering three times daily (14:00, 19:00, 23:00 UTC) to capture market movements without exhausting API limits.

---

## ⚠️ Disclaimer

**This project is strictly for educational and research purposes.**

PolyBot is a **paper-trading** simulator only. It does not connect to a crypto wallet, does not hold funds, and does not execute real-world transactions on Polymarket or any sportsbooks.

The +EV calculations and Kelly fractional sizing are theoretical and do not account for transaction fees, slippage, latency, or the inherent risks of decentralized markets. Do not use this code to risk real money.

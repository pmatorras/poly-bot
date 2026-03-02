# src/poly_bot/main.py
import argparse
from datetime import datetime

# Import the core functions from your other modules
from src.poly_bot.fetch_odds import main as fetch_odds_main
from src.poly_bot.edge_calculator import main as edge_calculator_main
from src.poly_bot.paper_trader import run_simulation as paper_trader_main

def log_step(step_name):
    print(f"\n{'='*50}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running: {step_name}")
    print(f"{'='*50}")

def main():
    parser = argparse.ArgumentParser(description="Polymarket NBA Arbitrage Bot")
    parser.add_argument('--run', choices=['fetch', 'analyze', 'resolve', 'morning_routine'], default='morning_routine', help="Which pipeline step to run")
    args = parser.parse_args()

    # 1. Resolve yesterday's pending bets
    if args.run in ['resolve', 'morning_routine']:
        log_step("paper_trader.py (Grading phase)")
        paper_trader_main()
        
    # 2. Fetch fresh odds from bookmakers
    if args.run in ['fetch', 'morning_routine']:
        log_step("fetch_odds.py")
        fetch_odds_main()
        
    # 3. Analyze Polymarket edges and place new mock bets
    if args.run in ['analyze', 'morning_routine']:
        log_step("edge_calculator.py")
        edge_calculator_main()
        # Call paper trader AGAIN here, but because we already graded, it will skip Phase 1 and immediately jump to Phase 2 (Sizing today's new bets)
        log_step("paper_trader.py (Sizing phase)")
        paper_trader_main()

if __name__ == "__main__":
    main()

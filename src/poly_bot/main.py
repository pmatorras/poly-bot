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
    parser.add_argument('--run', choices=['fetch', 'analyze', 'resolve', 'pipeline'], default='pipeline', help="Which pipeline step to run")
    args = parser.parse_args()

    # Resolve yesterday's pending bets
    if args.run in ['resolve', 'pipeline']:
        log_step("paper_trader.py (Grading phase)")
        paper_trader_main()
        
    # Fetch fresh odds from bookmakers
    if args.run in ['fetch', 'pipeline']:
        log_step("fetch_odds.py")
        fetch_odds_main()
        
    # Analyze Polymarket edges and place new mock bets
    if args.run in ['analyze', 'pipeline', 'check_poly']:
        log_step("edge_calculator.py")
        edge_calculator_main()
    if args.run in ['trade', 'pipeline', 'check_poly']:
        # Call paper trader to sizing today's new bets
        log_step("paper_trader.py (Sizing phase)")
        paper_trader_main()

if __name__ == "__main__":
    main()

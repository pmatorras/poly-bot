import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def run_script(script_name):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running {script_name}...")
    # Using subprocess allows you to keep the scripts completely decoupled
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error in {script_name}:\n{result.stderr}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Polymarket NBA Arbitrage Bot")
    parser.add_argument('--run', choices=['fetch', 'analyze', 'resolve', 'all', 'morning_routine'], 
                        default='morning_routine', help="Which pipeline step to run")
    args = parser.parse_args()

    if args.run in ['fetch', 'all', 'morning_routine']:
        run_script("fetch_odds.py")
        
    if args.run in ['analyze', 'all', 'morning_routine']:
        run_script("calculate_edges.py")
        
    if args.run in ['resolve', 'all']:
        # Resolves YESTERDAY'S pending bets
        run_script("paper_trader.py")

if __name__ == "__main__":
    main()

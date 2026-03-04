import pandas as pd
import requests
from datetime import datetime
from src.poly_bot.config import ODDS_API_KEY, TRADES_FILE, ABBR_MAP, ODDS_API_URL

STARTING_BANKROLL = 10000.0

def fetch_yesterdays_winners(sport):
    """Hits the Odds API /scores endpoint for a specific sport to find out who actually won."""
    
    # Extract the base sport string from the ODDS_API_URL in config
    # Example: "https://.../sports/basketball_nba/odds" -> "basketball_nba"
    odds_url = ODDS_API_URL.get(sport.lower())
    if not odds_url:
        print(f"No API URL configured for sport: {sport}")
        return {}
        
    api_sport_key = odds_url.split('/sports/')[1].replace('/odds', '')
    
    # Construct the correct /scores URL
    url = f"https://api.the-odds-api.com/v4/sports/{api_sport_key}/scores"
    params = {"apiKey": ODDS_API_KEY, "daysFrom": 1} # Look back 1 day
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch scores for {sport}.")
        return {}
        
    games = response.json()
    winners_map = {}
    
    # Get the abbreviation mapping for this specific sport
    sport_abbr_map = ABBR_MAP.get(sport.lower(), {})
    
    for game in games:
        if not game.get("completed"):
            continue
            
        home = game["home_team"]
        away = game["away_team"]
        
        # Apply the abbreviations to match the CSV format exactly
        home_abbr = sport_abbr_map.get(home, home).upper()
        away_abbr = sport_abbr_map.get(away, away).upper()
        
        game_key = f"{away_abbr} @ {home_abbr}"
        
        # Determine winner by looking at the scores array
        scores = game.get("scores", [])
        if scores and len(scores) == 2:
            score1 = int(scores[0]["score"])
            score2 = int(scores[1]["score"])
            
            if score1 > score2:
                winners_map[game_key] = scores[0]["name"]
            else:
                winners_map[game_key] = scores[1]["name"]
                
    return winners_map
def calculate_kelly_fraction(true_prob_pct, buy_price_pct, fraction=0.25):
    """Calculates the Quarter-Kelly recommended bet size."""
    p = true_prob_pct / 100.0
    q = 1.0 - p
    buy_price = buy_price_pct / 100.0
    
    # b = Net fractional odds (Payout - Investment) / Investment
    b = (1.0 - buy_price) / buy_price
    
    kelly_pct = ((b * p) - q) / b
    if kelly_pct <= 0: return 0.0
    return kelly_pct * fraction

def get_current_bankroll(df):
    """Calculates your current bankroll by summing all completed PnL."""
    if 'PnL_USD' in df.columns and not df['PnL_USD'].isna().all():
        total_profit = df['PnL_USD'].sum(skipna=True)
        return STARTING_BANKROLL + total_profit
    return STARTING_BANKROLL


# --- Core Logic Functions ---
def grade_yesterdays_bets(df):
    """Hits the API to resolve pending bets from previous days."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    mask_to_grade = (df['Status'] == 'PENDING') & (df['Date'] != today_str)
    pending_df = df[mask_to_grade]
    
    if pending_df.empty:
        print("No pending trades from previous days to grade.")
        return df
        
    print(f"Found {len(pending_df)} pending trades to grade. Fetching results...")
    # Find all unique sports that have pending trades
    sports_to_grade = pending_df['Sport'].str.lower().unique()

    # In a real run, this calls the fetch_yesterdays_winners() logic we wrote earlier
    all_actual_winners = {}
    for sport in sports_to_grade:
        winners = fetch_yesterdays_winners(sport)
        all_actual_winners.update(winners)    
    if not all_actual_winners:
        print("No completed games found in the API yet.")
        return df

    for index, row in pending_df.iterrows():
        game = row['Game']
        if game not in all_actual_winners:
            continue 
            
        is_win = (all_actual_winners[game] == row['Team_Bet_On'])
        bet_size = float(row['Bet_Size_USD'])
        buy_price_pct = float(row['Poly_Buy_Price_Pct'])
        
        if is_win:
            pnl = (bet_size / (buy_price_pct / 100.0)) - bet_size
        else:
            pnl = -bet_size
            
        df.at[index, 'Status'] = 'GRADED'
        df.at[index, 'Result'] = 'WON' if is_win else 'LOST'
        df.at[index, 'PnL_USD'] = round(pnl, 2)
        
    return df

def place_todays_bets(df):
    """Calculates Kelly sizing for newly appended, un-sized trades."""
    current_bankroll = get_current_bankroll(df)
    
    mask_to_place = (df['Status'] == 'PENDING') & (df['Bet_Size_USD'].isna())
    new_trades = df[mask_to_place]
    
    if new_trades.empty:
        print("No un-sized new bets to place right now.")
        return df
        
    print(f"\nSizing and placing {len(new_trades)} new mock bets...")
    print(f"Current Bankroll: ${current_bankroll:.2f}")
    
    for index, row in new_trades.iterrows():
        true_prob = float(row['Avg_Norm_SB_Prob'])
        buy_price_pct = float(row['Poly_Buy_Price_Pct'])
        liquidity = float(row['Available_Liquidity_USD'])
        
        kelly_pct = calculate_kelly_fraction(true_prob, buy_price_pct, fraction=0.25)
        desired_bet = current_bankroll * kelly_pct
        actual_bet = min(desired_bet, liquidity)
        
        df.at[index, 'Bet_Size_USD'] = round(actual_bet, 2)
        print(f" -> Placed ${actual_bet:.2f} on {row['Team_Bet_On']}")
        
    return df

# --- Entry Point ---
def run_simulation():
    try:
        # Add dtype parameter here to force 'Result' to be string
        df = pd.read_csv(TRADES_FILE, dtype={'Result': 'object', 'Status': 'object'})
    except FileNotFoundError:
        print(f"No {TRADES_FILE} found. Run calculate_edges.py first.")
        return


    # Pass the dataframe through the pipeline
    df = grade_yesterdays_bets(df)
    df = place_todays_bets(df)
    
    # Save once at the very end
    df.to_csv(TRADES_FILE, index=False)
    
    print("\n--- Pipeline Complete ---")
    print(f"Current Bankroll: ${get_current_bankroll(df):.2f}")

if __name__ == "__main__":
    run_simulation()

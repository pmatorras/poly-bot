import json
import requests
import pandas as pd
from datetime import datetime
import pytz

# --- Configuration ---
ODDS_CACHE_FILE = "nba_odds_cache.json"

# Map to translate Odds API full names into Polymarket's 3-letter abbreviations
NBA_ABBR = {
    "Atlanta Hawks": "atl", "Boston Celtics": "bos", "Brooklyn Nets": "bkn",
    "Charlotte Hornets": "cha", "Chicago Bulls": "chi", "Cleveland Cavaliers": "cle",
    "Dallas Mavericks": "dal", "Denver Nuggets": "den", "Detroit Pistons": "det",
    "Golden State Warriors": "gsw", "Houston Rockets": "hou", "Indiana Pacers": "ind",
    "Los Angeles Clippers": "lac", "Los Angeles Lakers": "lal", "Memphis Grizzlies": "mem",
    "Miami Heat": "mia", "Milwaukee Bucks": "mil", "Minnesota Timberwolves": "min",
    "New Orleans Pelicans": "nop", "New York Knicks": "nyk", "Oklahoma City Thunder": "okc",
    "Orlando Magic": "orl", "Philadelphia 76ers": "phi", "Phoenix Suns": "phx",
    "Portland Trail Blazers": "por", "Sacramento Kings": "sac", "San Antonio Spurs": "sas",
    "Toronto Raptors": "tor", "Utah Jazz": "uta", "Washington Wizards": "was"
}

def get_us_date(utc_time_str):
    """Converts Odds API UTC time to US Eastern date (used in Polymarket slugs)."""
    utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    eastern = pytz.timezone('US/Eastern')
    return utc_dt.astimezone(eastern).strftime("%Y-%m-%d")

def fetch_polymarket_by_slug(slug):
    """Hits Polymarket specifically for the single dynamically generated slug."""
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0] # Return the specific event
    return None

def main():
    # 1. Load your existing Odds API cache
    try:
        with open(ODDS_CACHE_FILE, "r", encoding="utf-8") as f:
            odds_games = json.load(f)
    except FileNotFoundError:
        print("Odds cache not found. Run the previous script to download it once.")
        return

    results = []
    
    for game in odds_games:
        home_team = game.get("home_team")
        away_team = game.get("away_team")
        
        if home_team not in NBA_ABBR or away_team not in NBA_ABBR:
            continue
            
        # 2. Extract and Average Sportsbook Odds
        if not game.get("bookmakers"):
            continue
            
        team_normalized_probs = {}
        
        # Loop through ALL bookmakers for this game
        for bm in game["bookmakers"]:
            if not bm.get("markets") or not bm["markets"][0].get("outcomes"):
                continue
                
            outcomes = bm["markets"][0]["outcomes"]
            if len(outcomes) != 2:
                continue
                
            # Get raw implied probabilities for this specific bookie
            prob_a = (1 / outcomes[0]["price"]) * 100
            prob_b = (1 / outcomes[1]["price"]) * 100
            
            # Calculate this specific bookie's vig/overround
            vig_sum = prob_a + prob_b
            
            # Normalize this bookie's odds to 100%
            norm_a = (prob_a / vig_sum) * 100
            norm_b = (prob_b / vig_sum) * 100
            
            team_a = outcomes[0]["name"]
            team_b = outcomes[1]["name"]
            
            # Append to our list
            if team_a not in team_normalized_probs: team_normalized_probs[team_a] = []
            if team_b not in team_normalized_probs: team_normalized_probs[team_b] = []
                
            team_normalized_probs[team_a].append(norm_a)
            team_normalized_probs[team_b].append(norm_b)
            
        # Calculate the final average normalized probability across all bookies
        sb_odds = {}
        for t, probs in team_normalized_probs.items():
            if probs:
                sb_odds[t] = sum(probs) / len(probs)
            
        # 3. Dynamically Generate Polymarket Slug!
        date_str = get_us_date(game["commence_time"])
        away_abbr = NBA_ABBR[away_team]
        home_abbr = NBA_ABBR[home_team]
        slug = f"nba-{away_abbr}-{home_abbr}-{date_str}"
        
        print(f"Checking {slug}...")
        poly_event = fetch_polymarket_by_slug(slug)
        
        if not poly_event:
            print(" -> Not found on Polymarket, skipping.")
            continue
            
                # 4. Extract Polymarket CLOB (Order Book) Prices
        poly_odds = {}
        for market in poly_event.get("markets", []):
            desc = market.get("description", "").lower()
            if "spread" in desc or "total" in desc:
                continue
                
            outcomes = json.loads(market.get("outcomes", "[]"))
            # We now grab the token IDs instead of the outcomePrices
            clob_tokens = json.loads(market.get("clobTokenIds", "[]")) 
            
            is_moneyline = False
            for full_team_name in sb_odds.keys():
                for i, outcome_str in enumerate(outcomes):
                    if outcome_str in full_team_name or full_team_name in outcome_str:
                        token_id = clob_tokens[i]
                        
                        # Hit the CLOB API for this specific team's token
                        clob_url = "https://clob.polymarket.com/book"
                        clob_resp = requests.get(clob_url, params={"token_id": token_id})
                        
                        if clob_resp.status_code == 200:
                            book = clob_resp.json()
                            asks = book.get('asks', [])
                            
                            if asks:
                                # Sort asks ascending (lowest price first)
                                sorted_asks = sorted(asks, key=lambda x: float(x['price']))
                                best_ask_price = float(sorted_asks[0]['price'])
                                
                                # Sum up all the shares available at this exact best price
                                # (Sometimes multiple users place orders at the same price)
                                available_shares = sum([
                                    float(ask['size']) for ask in sorted_asks 
                                    if float(ask['price']) == best_ask_price
                                ])
                                
                                # Calculate max dollar investment possible at this price
                                max_dollars = available_shares * best_ask_price
                                
                                poly_odds[full_team_name] = {
                                    "price_pct": round(best_ask_price * 100, 2),
                                    "max_dollars": round(max_dollars, 2)
                                }
                                is_moneyline = True
                                
            if is_moneyline and len(poly_odds) >= 2:
                break 
                
        # 5. Combine Data
        if len(sb_odds) == 2 and len(poly_odds) == 2:
            for team in sb_odds.keys():
                avg_norm_sb = sb_odds[team]
                # Use the exact actionable resting limit order from the book
                actionable_poly = poly_odds[team]['price_pct']
                actionable_vol = poly_odds[team]['max_dollars']
                results.append({
                    "Game": f"{away_abbr.upper()} @ {home_abbr.upper()}",
                    "Team": team,
                    "Avg_Norm_SB (%)": round(avg_norm_sb, 2),
                    "Actionable_Poly_Ask (%)": round(actionable_poly, 2),
                    "Trading_Edge (%)": round(avg_norm_sb - actionable_poly, 2), 
                    "Available volume ($)" : int(actionable_vol)
                })


    if results:
        df = pd.DataFrame(results).sort_values(by="Trading_Edge (%)", key=abs, ascending=False)
        print("\n--- TODAY'S MATCHES: POLYMARKET VS SPORTSBOOKS ---")
        print(df.to_string(index=False))
    else:
        print("No intersecting data found.")

if __name__ == "__main__":
    main()

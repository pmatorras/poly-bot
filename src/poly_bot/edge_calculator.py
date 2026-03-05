import os
import json
import requests
import pandas as pd
from datetime import datetime
import pytz
from src.poly_bot.config import MINIMUM_EDGE_THRESHOLD, TRADES_FILE, ODDS_CACHE_FILE, ABBR_MAP, POLYMARKET_TAGS


def save_opportunities_to_csv(results):
    """Filters for positive edges and appends them to the tracking CSV."""
    # Filter for viable trades
    valid_trades = []
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    for row in results:
        # Check if we have a positive edge greater than our threshold
        if row["Trading_Edge (%)"] >= MINIMUM_EDGE_THRESHOLD:
            
            # Format the dictionary for our CSV schema
            valid_trades.append({
                "Date": today_str,
                "Sport" : row["Sport"],
                "Game": row["Game"],
                "Team_Bet_On": row["Team"],
                "Avg_Norm_SB_Prob": row["Avg_Norm_SB (%)"],
                "Poly_Buy_Price_Pct": row["Actionable_Poly_Ask (%)"],
                "Trading_Edge_Pct": row["Trading_Edge (%)"],
                "Available_Liquidity_USD": row.get("Available_Liquidity ($)", 0.0),
                "Status": "PENDING", # Used by paper_trader.py to know it needs grading
                "Result": None,      # Will be updated to WON/LOST once the match finishes
                "Bet_Size_USD": None, # Filled by the paper_trader
                "PnL_USD": None       # Filled by the paper_trader
            })
            
    if not valid_trades:
        print("No actionable edges found today.")
        return
        
    df_new = pd.DataFrame(valid_trades)
    
    # Append to the CSV safely
    if os.path.exists(TRADES_FILE):
        # Load existing file
        df_existing = pd.read_csv(TRADES_FILE)
        
        # Build a set of already-logged keys — don't touch what exists
        existing_keys = set(
            zip(df_existing["Date"], df_existing["Game"], df_existing["Team_Bet_On"])
        )

        # Only keep truly new bets
        df_new = df_new[
            ~df_new.apply(
                lambda r: (r["Date"], r["Game"], r["Team_Bet_On"]) in existing_keys,
                axis=1
            )
        ]
        if df_new.empty:
            print("All opportunities already logged today, nothing to add.")
            return        
        # Combine and save
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(TRADES_FILE, index=False)
        print(f"Appended {len(df_new)} new opportunities to {TRADES_FILE}.")
    else:
        # Create the file for the first time
        df_new.to_csv(TRADES_FILE, index=False)
        print(f"Created {TRADES_FILE} with {len(df_new)} initial opportunities.")
        
    print("\n--- NEW TRADES ADDED ---")
    print(df_new.to_string(index=False))

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

def calculate_sport(sport, cache_file):
    """Processes edges for a single sport."""
    #if "ncaa" not in sport: return []

    print(f"\n--- Analyzing {sport.upper()} Edges ---")
    
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            odds_games = json.load(f)
    except FileNotFoundError:
        print(f"Odds cache not found for {sport}. Run fetch_odds.py first.")
        return [] # Return empty list so we don't break the main loop

    results = []
    sport_abbr = ABBR_MAP.get(sport, {})
    
    for game in odds_games:
        #print("game", game)
        home_team = game.get("home_team")
        away_team = game.get("away_team")
        
        if home_team not in sport_abbr or away_team not in sport_abbr:
            continue
            
        # 2. Extract and Average Sportsbook Odds
        if not game.get("bookmakers"):
            continue
            
        team_normalized_probs = {}
        
        for bm in game["bookmakers"]:
            if not bm.get("markets") or not bm["markets"][0].get("outcomes"):
                continue
                
            outcomes = bm["markets"][0]["outcomes"]
            if len(outcomes) != 2:
                continue
                
            prob_a = (1 / outcomes[0]["price"]) * 100
            prob_b = (1 / outcomes[1]["price"]) * 100
            
            vig_sum = prob_a + prob_b
            
            norm_a = (prob_a / vig_sum) * 100
            norm_b = (prob_b / vig_sum) * 100
            
            team_a = outcomes[0]["name"]
            team_b = outcomes[1]["name"]
            
            if team_a not in team_normalized_probs: team_normalized_probs[team_a] = []
            if team_b not in team_normalized_probs: team_normalized_probs[team_b] = []
                
            team_normalized_probs[team_a].append(norm_a)
            team_normalized_probs[team_b].append(norm_b)
            
        sb_odds = {}
        for t, probs in team_normalized_probs.items():
            if probs:
                sb_odds[t] = sum(probs) / len(probs)
            
        # 3. Dynamically Generate Polymarket Slug!
        date_str = get_us_date(game["commence_time"])
        away_abbr = sport_abbr[away_team]
        home_abbr = sport_abbr[home_team]
        
        # DYNAMIC SLUG GENERATION
        poly_tag = POLYMARKET_TAGS.get(sport, sport)
        slug = f"{poly_tag}-{away_abbr}-{home_abbr}-{date_str}"
        
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
            clob_tokens = json.loads(market.get("clobTokenIds", "[]")) 
            
            is_moneyline = False
            def normalize_name(name):
                return name.replace(" St ", " State ").replace("SE Louisiana", "Southeastern Louisiana")

            for full_team_name in sb_odds.keys():
                normalized_sb = normalize_name(full_team_name)
                for i, outcome_str in enumerate(outcomes):
                    normalized_poly = normalize_name(outcome_str)
                    if normalized_poly in normalized_sb or normalized_sb in normalized_poly:

                        #print(f"   SB teams: {list(sb_odds.keys())}")
                        #print(f"   Poly outcomes from API: {outcomes}")
                        print(f"   Poly odds matched: {poly_odds}")

                        token_id = clob_tokens[i]
                        
                        clob_url = "https://clob.polymarket.com/book"
                        clob_resp = requests.get(clob_url, params={"token_id": token_id})
                        
                        if clob_resp.status_code == 200:
                            book = clob_resp.json()
                            asks = book.get('asks', [])
                            
                            if asks:
                                sorted_asks = sorted(asks, key=lambda x: float(x['price']))
                                best_ask_price = float(sorted_asks[0]['price'])
                                
                                available_shares = sum([
                                    float(ask['size']) for ask in sorted_asks 
                                    if float(ask['price']) == best_ask_price
                                ])
                                
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
                actionable_poly = poly_odds[team]['price_pct']
                actionable_vol = poly_odds[team]['max_dollars']
                results.append({
                    "Sport": sport.upper(), 
                    "Game": f"{away_abbr.upper()} @ {home_abbr.upper()}",
                    "Team": team,
                    "Avg_Norm_SB (%)": round(avg_norm_sb, 2),
                    "Actionable_Poly_Ask (%)": round(actionable_poly, 2),
                    "Trading_Edge (%)": round(avg_norm_sb - actionable_poly, 2), 
                    "Available_Liquidity ($)" : int(actionable_vol)
                })
                
    return results

def main():
    all_results = []
    
    # Iterate through the config dictionary
    for sport, cache_file in ODDS_CACHE_FILE.items():
        sport_results = calculate_sport(sport, cache_file)
        all_results.extend(sport_results)
        
    # Process and save everything together at the end
    if all_results:
        df = pd.DataFrame(all_results).sort_values(by="Trading_Edge (%)", key=abs, ascending=False)
        print("\n--- TODAY'S MATCHES: POLYMARKET VS SPORTSBOOKS ---")
        print(df.to_string(index=False))
        save_opportunities_to_csv(all_results)
    else:
        print("\nNo intersecting data found across any sports.")

if __name__ == "__main__":
    main()

    
if __name__ == "__main__":
    main()

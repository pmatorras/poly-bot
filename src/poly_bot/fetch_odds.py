import os
import time
import json
import requests
from src.poly_bot.config import ODDS_API_KEY, ODDS_API_URL, ODDS_CACHE_FILE

# How old the cache can be before we force a new download
CACHE_STALE_HOURS = 12

def fetch_or_load_cache(file_path, fetch_function):
    """Loads data from a local JSON cache, but fetches live if missing or stale."""
    
    # 1. Check if the file exists AND if it is fresh
    if os.path.exists(file_path):
        file_stat = os.stat(file_path)
        last_modified_time = file_stat.st_mtime
        current_time = time.time()
        
        # Calculate age in hours
        age_in_hours = (current_time - last_modified_time) / 3600
        
        if age_in_hours < CACHE_STALE_HOURS:
            print(f"Loading fresh cache ({age_in_hours:.1f} hours old): {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"Cache is stale ({age_in_hours:.1f} hours old). Force refreshing...")
    else:
        print(f"Cache not found. Fetching live data for {file_path}...")

    # 2. Fetch live data (either because file is missing or stale)
    data = fetch_function()
    
    # Save the new data, which automatically resets the file's modified timestamp
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    return data

def fetch_live_sportsbook_data(source='nba'):
    """Makes the actual HTTP request to The Odds API."""
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }
    response = requests.get(ODDS_API_URL[source], params=params)
    response.raise_for_status()
    return response.json()

def main():
    print("Checking sportsbook data status...")
    
    for source in ODDS_CACHE_FILE.keys():
        print(f"\n--- Processing {source.upper()} ---")
        
        # Use a lambda to pass the specific source without executing it immediately
        fetch_func = lambda s=source: fetch_live_sportsbook_data(s)
        
        # Pass the dictionary value for the file, and the lambda for the function
        raw_sb_data = fetch_or_load_cache(ODDS_CACHE_FILE[source], fetch_func)
        
        print(f"Successfully loaded {len(raw_sb_data)} {source.upper()} games.")


if __name__ == "__main__":
    main()

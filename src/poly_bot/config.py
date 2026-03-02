import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
print(PROJECT_ROOT)
# Define the data directory
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Configuration ---
ODDS_CACHE_FILE = {
    "nba" : DATA_DIR / "nba_odds_cache.json",
    "nhl" : DATA_DIR / "nhl_odds_cache.json",
}
TRADES_FILE = DATA_DIR / "paper_trades.csv"
MINIMUM_EDGE_THRESHOLD = 1.0  # Only log trades if the edge is > 1.0%
ODDS_API_KEY = os.getenv('ODDS_API_KEY')
ODDS_API_URL = {
    "nba" : "https://api.the-odds-api.com/v4/sports/basketball_nba/odds",
    "nhl": "https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds",
}
# Map to translate Odds API full names into Polymarket's 3-letter abbreviations
ABBR_MAP = {
    'nba' : {
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
    },
    "nhl": {
        "Anaheim Ducks": "ana", "Boston Bruins": "bos", "Buffalo Sabres": "buf",
        "Calgary Flames": "cgy", "Carolina Hurricanes": "car", "Chicago Blackhawks": "chi",
        "Colorado Avalanche": "col", "Columbus Blue Jackets": "cbj", "Dallas Stars": "dal",
        "Detroit Red Wings": "det", "Edmonton Oilers": "edm", "Florida Panthers": "fla",
        "Los Angeles Kings": "la", "Minnesota Wild": "min", "Montreal Canadiens": "mtl",
        "Nashville Predators": "nsh", "New Jersey Devils": "nj", "New York Islanders": "nyi",
        "New York Rangers": "nyr", "Ottawa Senators": "ott", "Philadelphia Flyers": "phi",
        "Pittsburgh Penguins": "pit", "San Jose Sharks": "sj", "Seattle Kraken": "sea",
        "St Louis Blues": "stl", "Tampa Bay Lightning": "tb", "Toronto Maple Leafs": "tor",
        "Utah Hockey Club": "uta", "Vancouver Canucks": "van", "Vegas Golden Knights": "vgk",
        "Washington Capitals": "wsh", "Winnipeg Jets": "wpg"
    }
}
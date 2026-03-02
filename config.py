import os

# --- Configuration ---
ODDS_CACHE_FILE = "nba_odds_cache.json"
TRADES_FILE = "paper_trades.csv"
MINIMUM_EDGE_THRESHOLD = 1.0  # Only log trades if the edge is > 1.0%
ODDS_API_KEY = os.getenv('ODDS_API_KEY')
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

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
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
    "ncaab" : DATA_DIR / "ncaab_odds_cache.json",
}
TRADES_FILE = DATA_DIR / "paper_trades.csv"
MINIMUM_EDGE_THRESHOLD = 1.0  # Only log trades if the edge is > 1.0%
ODDS_API_KEY = os.getenv('ODDS_API_KEY')
ODDS_API_URL = {
    "nba" : "https://api.the-odds-api.com/v4/sports/basketball_nba/odds",
    "nhl": "https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds",
    "ncaab": "https://api.the-odds-api.com/v4/sports/basketball_ncaab/odds",
}

POLYMARKET_TAGS = {
    "nba": "nba",
    "nhl": "nhl",
    "ncaab": "cbb"
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
    },
    'ncaab': {
        # NOT FOUND ON POLYMARKET: "Arizona Wildcats"
        # NOT FOUND ON POLYMARKET: "Cleveland St Vikings"
        "Coppin St Eagles": "coppst",
        # NOT FOUND ON POLYMARKET: "Delaware St Hornets"
        "Duke Blue Devils": "duke",  # guessed, verify manually
        "East Texas A&M Lions": "tamu",
        # NOT FOUND ON POLYMARKET: "Eastern Washington Eagles"
        "Houston Christian Huskies": "houbap",
        "Howard Bison": "howrd",  # guessed, verify manually
        "IUPUI Jaguars": "iupui",
        # NOT FOUND ON POLYMARKET: "Idaho State Bengals"
        "Idaho Vandals": "idaho",
        # NOT FOUND ON POLYMARKET: "Incarnate Word Cardinals"
        "Iowa State Cyclones": "iowast",
        "Lamar Cardinals": "lamar",
        "Maryland-Eastern Shore Hawks": "mdes",
        "McNeese Cowboys": "mcnst",  # guessed, verify manually
        "Montana Grizzlies": "monst",  # guessed, verify manually
        "Montana St Bobcats": "mont",  # guessed, verify manually
        "Morgan St Bears": "morgst",
        "N Colorado Bears": "ncol",
        "NC State Wolfpack": "ncst",
        "New Orleans Privateers": "no",
        # NOT FOUND ON POLYMARKET: "Nicholls St Colonels"
        "Norfolk St Spartans": "norfst",
        "North Carolina Central Eagles": "ncc",
        "Northern Arizona Lumberjacks": "no",  # guessed, verify manually
        "Northwestern St Demons": "no",  # guessed, verify manually
        "Portland St Vikings": "portst",
        "SE Louisiana Lions": "selou",
        # NOT FOUND ON POLYMARKET: "Sacramento St Hornets"
        # NOT FOUND ON POLYMARKET: "South Carolina St Bulldogs"
        "Stephen F. Austin Lumberjacks": "sfaus",
        # NOT FOUND ON POLYMARKET: "Texas A&M-CC Islanders"
        "UT Rio Grande Valley Vaqueros": "utrgv",
        # NOT FOUND ON POLYMARKET: "Weber State Wildcats",
        "Arkansas Razorbacks": "ark",
        # NOT FOUND ON POLYMARKET: "Arkansas-Little Rock Trojans"
        # NOT FOUND ON POLYMARKET: "Baylor Bears"
        "Bellarmine Knights": "bella",  # guessed, verify manually
        "Butler Bulldogs": "butl",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "California Golden Bears"
        # NOT FOUND ON POLYMARKET: "Central Connecticut St Blue Devils"
        "Charlotte 49ers": "charlt",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Chicago St Cougars"
        # NOT FOUND ON POLYMARKET: "Cleveland St Vikings"
        # NOT FOUND ON POLYMARKET: "Colorado St Rams"
        "Creighton Bluejays": "creigh",  # guessed, verify manually
        "Davidson Wildcats": "david",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "DePaul Blue Demons"
        "Detroit Mercy Titans": "det",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Duquesne Dukes"
        # NOT FOUND ON POLYMARKET: "Eastern Illinois Panthers"
        # NOT FOUND ON POLYMARKET: "Eastern Kentucky Colonels"
        # NOT FOUND ON POLYMARKET: "Fairleigh Dickinson Knights"
        # NOT FOUND ON POLYMARKET: "Florida Gulf Coast Eagles"
        # NOT FOUND ON POLYMARKET: "Florida St Seminoles"
        "Fordham Rams": "fordm",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "GW Revolutionaries"
        # NOT FOUND ON POLYMARKET: "Gardner-Webb Bulldogs"
        # NOT FOUND ON POLYMARKET: "Georgia Southern Eagles"
        # NOT FOUND ON POLYMARKET: "Georgia Tech Yellow Jackets"
        # NOT FOUND ON POLYMARKET: "Houston Cougars"
        "Indiana Hoosiers": "ind",
        # NOT FOUND ON POLYMARKET: "Jacksonville Dolphins"
        # NOT FOUND ON POLYMARKET: "James Madison Dukes"
        "LIU Sharks": "liub",  # guessed, verify manually
        "La Salle Explorers": "lasal",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Le Moyne Dolphins"
        # NOT FOUND ON POLYMARKET: "Lindenwood Lions"
        # NOT FOUND ON POLYMARKET: "Louisiana Ragin' Cajuns"
        # NOT FOUND ON POLYMARKET: "Loyola (Chi) Ramblers"
        "Marquette Golden Eagles": "marq",  # guessed, verify manually
        "Maryland Terrapins": "marq",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Mercyhurst Lakers"
        "Miami (OH) RedHawks": "mia",  # guessed, verify manually
        "Miami Hurricanes": "mia",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Milwaukee Panthers"
        # NOT FOUND ON POLYMARKET: "Minnesota Golden Gophers"
        # NOT FOUND ON POLYMARKET: "New Mexico Lobos"
        # NOT FOUND ON POLYMARKET: "North Alabama Lions"
        # NOT FOUND ON POLYMARKET: "North Florida Ospreys"
        # NOT FOUND ON POLYMARKET: "North Texas Mean Green"
        # NOT FOUND ON POLYMARKET: "Northern Kentucky Norse"
        # NOT FOUND ON POLYMARKET: "Northwestern Wildcats"
        # NOT FOUND ON POLYMARKET: "Notre Dame Fighting Irish"
        "Oakland Golden Grizzlies": "oak",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Ohio Bobcats"
        # NOT FOUND ON POLYMARKET: "Ohio State Buckeyes"
        # NOT FOUND ON POLYMARKET: "Old Dominion Monarchs"
        # NOT FOUND ON POLYMARKET: "Oral Roberts Golden Eagles"
        # NOT FOUND ON POLYMARKET: "Penn State Nittany Lions"
        # NOT FOUND ON POLYMARKET: "Pittsburgh Panthers"
        "Providence Friars": "prov",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Purdue Boilermakers"
        # NOT FOUND ON POLYMARKET: "Rhode Island Rams"
        # NOT FOUND ON POLYMARKET: "Rice Owls"
        # NOT FOUND ON POLYMARKET: "Robert Morris Colonials"
        "SIU-Edwardsville Cougars": "siue",  # guessed, verify manually
        "SMU Mustangs": "smu",
        # NOT FOUND ON POLYMARKET: "Saint Joseph's Hawks"
        # NOT FOUND ON POLYMARKET: "Saint Louis Billikens"
        # NOT FOUND ON POLYMARKET: "South Carolina Upstate Spartans"
        # NOT FOUND ON POLYMARKET: "St. Bonaventure Bonnies"
        # NOT FOUND ON POLYMARKET: "Stanford Cardinal"
        "Stetson Hatters": "stetsn",  # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Stonehill Skyhawks"
        # NOT FOUND ON POLYMARKET: "Texas Longhorns"
        # NOT FOUND ON POLYMARKET: "UMKC Kangaroos"
        # NOT FOUND ON POLYMARKET: "USC Trojans"
        # NOT FOUND ON POLYMARKET: "Villanova Wildcats"
        # NOT FOUND ON POLYMARKET: "Wagner Seahawks"
        # NOT FOUND ON POLYMARKET: "Washington Huskies"
        # NOT FOUND ON POLYMARKET: "West Georgia Wolves"
        # NOT FOUND ON POLYMARKET: "Wisconsin Badgers"
        # NOT FOUND ON POLYMARKET: "Wright St Raiders"
        # NOT FOUND ON POLYMARKET: "Youngstown St Penguins"
        "UAB Blazers": "uab",
        # NOT FOUND ON POLYMARKET: "Iowa Hawkeyes"
        # NOT FOUND ON POLYMARKET: "Michigan St Spartans"
        # NOT FOUND ON POLYMARKET: "Michigan Wolverines"
        # NOT FOUND ON POLYMARKET: "Rutgers Scarlet Knights"
    }
}
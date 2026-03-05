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
        # NOT FOUND ON POLYMARKET: "Abilene Christian Wildcats"
        # NOT FOUND ON POLYMARKET: "CSU Bakersfield Roadrunners"
        # NOT FOUND ON POLYMARKET: "CSU Fullerton Titans"
        # NOT FOUND ON POLYMARKET: "CSU Northridge Matadors"
        # NOT FOUND ON POLYMARKET: "Cal Baptist Lancers"
        # NOT FOUND ON POLYMARKET: "Cal Poly Mustangs"
        # NOT FOUND ON POLYMARKET: "Delaware Blue Hens"
        # NOT FOUND ON POLYMARKET: "Drake Bulldogs"
        # NOT FOUND ON POLYMARKET: "East Carolina Pirates"
        # NOT FOUND ON POLYMARKET: "Evansville Purple Aces"
        # NOT FOUND ON POLYMARKET: "Fairfield Stags"
        # NOT FOUND ON POLYMARKET: "Florida Int'l Golden Panthers"
        # NOT FOUND ON POLYMARKET: "Hawai'i Rainbow Warriors"
        "Indiana St Sycamores": "ind", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Iona Gaels"
        # NOT FOUND ON POLYMARKET: "Jacksonville St Gamecocks"
        # NOT FOUND ON POLYMARKET: "Kennesaw St Owls"
        # NOT FOUND ON POLYMARKET: "Liberty Flames"
        # NOT FOUND ON POLYMARKET: "Long Beach St 49ers"
        # NOT FOUND ON POLYMARKET: "Louisiana Tech Bulldogs"
        # NOT FOUND ON POLYMARKET: "Loyola Marymount Lions"
        # NOT FOUND ON POLYMARKET: "Manhattan Jaspers"
        # NOT FOUND ON POLYMARKET: "Memphis Tigers"
        # NOT FOUND ON POLYMARKET: "Middle Tennessee Blue Raiders"
        # NOT FOUND ON POLYMARKET: "Missouri St Bears"
        # NOT FOUND ON POLYMARKET: "New Mexico St Aggies"
        # NOT FOUND ON POLYMARKET: "Northern Iowa Panthers"
        # NOT FOUND ON POLYMARKET: "Pepperdine Waves"
        # NOT FOUND ON POLYMARKET: "Portland Pilots"
        # NOT FOUND ON POLYMARKET: "Sacred Heart Pioneers"
        # NOT FOUND ON POLYMARKET: "Sam Houston St Bearkats"
        # NOT FOUND ON POLYMARKET: "San Diego Toreros"
        # NOT FOUND ON POLYMARKET: "South Dakota St Jackrabbits"
        # NOT FOUND ON POLYMARKET: "South Florida Bulls"
        # NOT FOUND ON POLYMARKET: "Southern Illinois Salukis"
        # NOT FOUND ON POLYMARKET: "Southern Utah Thunderbirds"
        # NOT FOUND ON POLYMARKET: "St. Thomas (MN) Tommies"
        # NOT FOUND ON POLYMARKET: "Tarleton State Texans"
        # NOT FOUND ON POLYMARKET: "Temple Owls"
        # NOT FOUND ON POLYMARKET: "Tulane Green Wave"
        # NOT FOUND ON POLYMARKET: "Tulsa Golden Hurricane"
        # NOT FOUND ON POLYMARKET: "UC Davis Aggies"
        # NOT FOUND ON POLYMARKET: "UC Irvine Anteaters"
        "UC Riverside Highlanders": "ri", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "UC San Diego Tritons"
        # NOT FOUND ON POLYMARKET: "UT-Arlington Mavericks"
        # NOT FOUND ON POLYMARKET: "UTEP Miners"
        # NOT FOUND ON POLYMARKET: "Utah Valley Wolverines"
        # NOT FOUND ON POLYMARKET: "Valparaiso Beacons"
        # NOT FOUND ON POLYMARKET: "Western Kentucky Hilltoppers"
        # NOT FOUND ON POLYMARKET: "Alabama A&M Bulldogs"
        # NOT FOUND ON POLYMARKET: "Alabama St Hornets"
        # NOT FOUND ON POLYMARKET: "Alcorn St Braves"
        "American Eagles": "amercn", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Arkansas St Red Wolves"
        # NOT FOUND ON POLYMARKET: "Arkansas-Pine Bluff Golden Lions"
        # NOT FOUND ON POLYMARKET: "Bethune-Cookman Wildcats"
        "Boston Univ. Terriers": "bostu", # guessed, verify manually
        "Bucknell Bison": "buck", # guessed, verify manually
        "Colgate Raiders": "colg", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Florida A&M Rattlers"
        "Grambling St Tigers": "mst", # guessed, verify manually
        "Holy Cross Crusaders": "holy", # guessed, verify manually
        "Jackson St Tigers": "jackst",
        "Lehigh Mountain Hawks": "lehi", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Loyola (MD) Greyhounds"
        # NOT FOUND ON POLYMARKET: "Miss Valley St Delta Devils"
        "Navy Midshipmen": "navy",
        # NOT FOUND ON POLYMARKET: "North Dakota St Bison"
        # NOT FOUND ON POLYMARKET: "Prairie View Panthers"
        # NOT FOUND ON POLYMARKET: "SE Missouri St Redhawks"
        # NOT FOUND ON POLYMARKET: "Southern Jaguars"
        # NOT FOUND ON POLYMARKET: "Southern Miss Golden Eagles"
        # NOT FOUND ON POLYMARKET: "Tenn-Martin Skyhawks"
        # NOT FOUND ON POLYMARKET: "Texas Southern Tigers"
        # NOT FOUND ON POLYMARKET: "Missouri Tigers"
        # NOT FOUND ON POLYMARKET: "Akron Zips"
        # NOT FOUND ON POLYMARKET: "Austin Peay Governors"
        # NOT FOUND ON POLYMARKET: "Ball State Cardinals"
        # NOT FOUND ON POLYMARKET: "Bowling Green Falcons"
        # NOT FOUND ON POLYMARKET: "Brown Bears"
        # NOT FOUND ON POLYMARKET: "Buffalo Bulls"
        # NOT FOUND ON POLYMARKET: "Central Arkansas Bears"
        # NOT FOUND ON POLYMARKET: "Central Michigan Chippewas"
        # NOT FOUND ON POLYMARKET: "Charleston Southern Buccaneers"
        # NOT FOUND ON POLYMARKET: "Chattanooga Mocs"
        "Columbia Lions": "colg", # guessed, verify manually
        # NOT FOUND ON POLYMARKET: "Dayton Flyers"
        # NOT FOUND ON POLYMARKET: "Denver Pioneers"
        # NOT FOUND ON POLYMARKET: "Eastern Michigan Eagles"
        # NOT FOUND ON POLYMARKET: "Harvard Crimson"
        # NOT FOUND ON POLYMARKET: "High Point Panthers"
        # NOT FOUND ON POLYMARKET: "Kent State Golden Flashes"
        # NOT FOUND ON POLYMARKET: "Lipscomb Bisons"
        # NOT FOUND ON POLYMARKET: "Longwood Lancers"
        # NOT FOUND ON POLYMARKET: "Murray St Racers"
        # NOT FOUND ON POLYMARKET: "North Carolina A&T Aggies"
        # NOT FOUND ON POLYMARKET: "North Dakota Fighting Hawks"
        # NOT FOUND ON POLYMARKET: "Northeastern Huskies"
        # NOT FOUND ON POLYMARKET: "Northern Illinois Huskies"
        # NOT FOUND ON POLYMARKET: "Omaha Mavericks"
        # NOT FOUND ON POLYMARKET: "Pennsylvania Quakers"
        # NOT FOUND ON POLYMARKET: "Presbyterian Blue Hose"
        # NOT FOUND ON POLYMARKET: "Queens University Royals"
        # NOT FOUND ON POLYMARKET: "Radford Highlanders"
        # NOT FOUND ON POLYMARKET: "San Diego St Aztecs"
        # NOT FOUND ON POLYMARKET: "Seton Hall Pirates"
        # NOT FOUND ON POLYMARKET: "South Dakota Coyotes"
        # NOT FOUND ON POLYMARKET: "St. John's Red Storm"
        # NOT FOUND ON POLYMARKET: "The Citadel Bulldogs"
        # NOT FOUND ON POLYMARKET: "Toledo Rockets"
        # NOT FOUND ON POLYMARKET: "UCF Knights"
        # NOT FOUND ON POLYMARKET: "UIC Flames"
        # NOT FOUND ON POLYMARKET: "UNC Asheville Bulldogs"
        # NOT FOUND ON POLYMARKET: "UNC Greensboro Spartans"
        # NOT FOUND ON POLYMARKET: "UNLV Rebels"
        # NOT FOUND ON POLYMARKET: "VCU Rams"
        # NOT FOUND ON POLYMARKET: "VMI Keydets"
        # NOT FOUND ON POLYMARKET: "West Virginia Mountaineers"
        # NOT FOUND ON POLYMARKET: "Western Michigan Broncos"
        # NOT FOUND ON POLYMARKET: "Winthrop Eagles"
    }
}
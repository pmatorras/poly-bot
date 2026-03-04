import json
import re
import requests
from src.poly_bot import config
from src.poly_bot.config import ODDS_CACHE_FILE, ABBR_MAP

def auto_generate_daily_map():
    # Load odds cache
    with open(ODDS_CACHE_FILE['ncaab'], "r") as f:
        odds_data = json.load(f)

    odds_teams = set()
    for game in odds_data:
        h = game.get("home_team") or game.get("hometeam")
        a = game.get("away_team") or game.get("awayteam")
        if h: odds_teams.add(h)
        if a: odds_teams.add(a)

    # Filter out teams already present in config.py
    existing_teams = set(ABBR_MAP.get('ncaab', {}).keys())

    # Parse config.py text to find teams already marked as NOT FOUND or FAILED
    config_path = config.__file__
    if config_path.endswith('.pyc'):
        config_path = config_path[:-1]

    with open(config_path, "r") as f:
        config_text = f.read()

    not_found = re.findall(r'# NOT FOUND ON POLYMARKET:\s*"([^"]+)"', config_text)
    failed = re.findall(r'# FAILED TO GENERATE ABBR:\s*"([^"]+)"', config_text)
    
    existing_teams.update(not_found)
    existing_teams.update(failed)

    # Now filter odds_teams
    new_teams = [t for t in sorted(odds_teams) if t not in existing_teams]

    if not new_teams:
        print("No new NCAAB teams to add.")
        return

    # Scrape Polymarket live games page for URL patterns
    url = "https://polymarket.com/sports/cbb/games"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html = response.text

    pattern = r'/sports/cbb/cbb-([a-z0-9]+)-([a-z0-9]+)-\d{4}-\d{2}-\d{2}'
    matches = re.findall(pattern, html)

    poly_abbrs = set()
    for team1, team2 in matches:
        poly_abbrs.add(team1)
        poly_abbrs.add(team2)

    # Generate new formatting 
    def generate_abbr(team_name):
        """Generate Polymarket-style abbreviation"""
        # Normalize common patterns
        name = team_name.replace(" St ", " State ")
        name = name.replace("-", " ")
        
        # Special cases
        if "IUPUI" in name:
            return "iupui"
        if "NC State" in name or "North Carolina State" in name:
            return "ncst"
        if "N Colorado" in name:
            return "ncol"
        if "New Orleans" in name:
            return "no"
        if "SE Louisiana" in name:
            return "selou"
        if "UT Rio Grande" in name:
            return "utrgv"
        if "Texas A&M-CC" in name or "Texas A&M Corpus" in name:
            return "txamc"
        if "East Texas A&M" in name:
            return "tamu"
        if "Houston Christian" in name or "Houston Baptist" in name:
            return "houbap"
        if "Stephen F. Austin" in name:
            return "sfaus"
        if "Maryland Eastern Shore" in name:
            return "mdes"
        if "North Carolina Central" in name:
            return "ncc"
        
        # Remove mascot (last word)
        words = [w for w in name.split() if w not in ['the', 'of', 'and']]
        words = words[:-1]  # Drop mascot
        
        if len(words) == 1:
            # Single word: "Duke" -> "duke", "Arizona" -> "arz" (first 3-4 letters)
            w = words[0].lower()
            return w if len(w) <= 5 else w[:3]
        elif len(words) == 2:
            # Two words: "Norfolk State" -> "norf" + "st" = "norfst"
            return words[0][:4].lower() + words[1][:2].lower()
        else:
            # Three+ words: take first 2-3 letters each
            return ''.join(w[:2].lower() for w in words[:3])

    new_lines = []
    for team in new_teams:
        abbr = generate_abbr(team)
        
        # Safeguard if a weird team name resolves to an empty string in the logic above
        if not abbr:
            new_lines.append(f'        # FAILED TO GENERATE ABBR: "{team}"\n')
            continue

        if abbr in poly_abbrs:
            new_lines.append(f'        "{team}": "{abbr}",\n')
        else:
            closest = next((pa for pa in poly_abbrs if pa in abbr or abbr in pa), None)
            if closest:
                new_lines.append(f'        "{team}": "{closest}", # guessed, verify manually\n')
            else:
                new_lines.append(f'        # NOT FOUND ON POLYMARKET: "{team}"\n')

    # Append missing entries back to config.py safely
    lines = config_text.splitlines(True)
    ncaab_start = next((i for i, line in enumerate(lines) if "'ncaab': {" in line or '"ncaab": {' in line), -1)

    if ncaab_start != -1:
        brace_count = 0
        insert_idx = -1
        for i in range(ncaab_start, len(lines)):
            brace_count += lines[i].count('{')
            brace_count -= lines[i].count('}')
            if brace_count == 0:
                insert_idx = i
                break
        
        if insert_idx != -1:
            lines = lines[:insert_idx] + new_lines + lines[insert_idx:]
            with open(config_path, "w") as f:
                f.writelines(lines)
            print(f"Successfully appended {len(new_lines)} new teams to config.py.")
        else:
            print("Error: Could not find the closing brace for the 'ncaab' dict.")
    else:
        print("Error: Could not locate the 'ncaab' dictionary block in config.py.")

if __name__ == "__main__":
    auto_generate_daily_map()

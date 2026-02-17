#!/usr/bin/env python3
"""
Get NBA Team Schedule - Shows upcoming games
Uses ESPN's public API (free, no authentication required)
"""

import sys
import requests
from datetime import datetime, timedelta
import json

# Team abbreviation mapping (ESPN uses different abbreviations)
TEAM_ABBR_MAP = {
    'lakers': 'LAL', 'celtics': 'BOS', 'warriors': 'GS', 'heat': 'MIA',
    'bucks': 'MIL', 'nuggets': 'DEN', 'suns': 'PHX', '76ers': 'PHI', 'sixers': 'PHI',
    'mavericks': 'DAL', 'mavs': 'DAL', 'clippers': 'LAC', 'grizzlies': 'MEM',
    'pelicans': 'NO', 'blazers': 'POR', 'trail blazers': 'POR',
    'kings': 'SAC', 'spurs': 'SA', 'thunder': 'OKC', 'jazz': 'UTAH',
    'timberwolves': 'MIN', 'wolves': 'MIN', 'bulls': 'CHI', 'cavaliers': 'CLE',
    'cavs': 'CLE', 'hawks': 'ATL', 'hornets': 'CHA', 'magic': 'ORL',
    'pacers': 'IND', 'pistons': 'DET', 'raptors': 'TOR', 'wizards': 'WSH',
    'nets': 'BKN', 'knicks': 'NY', 'rockets': 'HOU'
}

# ESPN team IDs
ESPN_TEAM_IDS = {
    'ATL': '01', 'BOS': '02', 'BKN': '17', 'CHA': '30', 'CHI': '04', 'CLE': '05',
    'DAL': '06', 'DEN': '07', 'DET': '08', 'GS': '09', 'HOU': '10', 'IND': '11',
    'LAC': '12', 'LAL': '13', 'MEM': '29', 'MIA': '14', 'MIL': '15', 'MIN': '16',
    'NO': '03', 'NY': '18', 'OKC': '25', 'ORL': '19', 'PHI': '20', 'PHX': '21',
    'POR': '22', 'SAC': '23', 'SA': '24', 'TOR': '28', 'UTAH': '26', 'WSH': '27'
}


def get_team_abbr(team_name):
    """Convert team name to ESPN abbreviation"""
    team_lower = team_name.lower()

    # Check if it's already an abbreviation
    if team_name.upper() in ESPN_TEAM_IDS:
        return team_name.upper()

    # Search in mapping
    for key, abbr in TEAM_ABBR_MAP.items():
        if key in team_lower:
            return abbr

    return None


def get_team_schedule(team_abbr, num_games=10):
    """
    Get upcoming schedule for a team using ESPN API

    Args:
        team_abbr: Team abbreviation (e.g., 'LAL', 'BOS')
        num_games: Number of upcoming games to fetch

    Returns:
        List of upcoming games with opponent, date, home/away
    """
    team_id = ESPN_TEAM_IDS.get(team_abbr)
    if not team_id:
        return None

    # ESPN API endpoint for team schedule
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"❌ Error: ESPN API returned status {response.status_code}")
            return None

        data = response.json()

        if 'events' not in data:
            print(f"❌ Error: No schedule data found")
            return None

        upcoming_games = []
        # Use UTC for comparison to avoid timezone issues
        from datetime import timezone
        current_date = datetime.now(timezone.utc)

        for event in data['events']:
            game_date_str = event['date']
            # ESPN returns UTC times
            game_date = datetime.fromisoformat(game_date_str.replace('Z', '+00:00'))

            # Only include future games (compare in UTC)
            if game_date > current_date:
                competitions = event['competitions'][0]
                competitors = competitions['competitors']

                # Figure out home/away
                home_team = None
                away_team = None

                for comp in competitors:
                    team_info = comp['team']
                    if comp['homeAway'] == 'home':
                        home_team = team_info['abbreviation']
                    else:
                        away_team = team_info['abbreviation']

                # Determine if our team is home or away
                is_home = (home_team == team_abbr)
                opponent = away_team if is_home else home_team

                upcoming_games.append({
                    'date': game_date,
                    'opponent': opponent,
                    'home_away': 'vs' if is_home else '@',
                    'full_matchup': f"{team_abbr} vs {opponent}" if is_home else f"{team_abbr} @ {opponent}"
                })

                if len(upcoming_games) >= num_games:
                    break

        return upcoming_games

    except Exception as e:
        print(f"❌ Error fetching schedule: {str(e)}")
        return None


def display_schedule(team_name, num_games=10):
    """Display upcoming schedule for a team"""
    print("\n" + "="*70)
    print(f"📅 UPCOMING SCHEDULE: {team_name}")
    print("="*70)

    team_abbr = get_team_abbr(team_name)
    if not team_abbr:
        print(f"❌ Unknown team: {team_name}")
        print("   Try: Lakers, Celtics, Warriors, Heat, etc.")
        return

    print(f"\nFetching schedule for {team_abbr}...")

    games = get_team_schedule(team_abbr, num_games)

    if not games:
        print(f"❌ Could not fetch schedule for {team_name}")
        print("   ESPN API might be temporarily unavailable")
        return

    if len(games) == 0:
        print(f"\n✓ No upcoming games found for {team_name}")
        print("   (Season might be over or on break)")
        return

    print(f"\n✓ Found {len(games)} upcoming games:")
    print(f"   (Note: Dates shown in UTC - may be off by 1 day depending on your timezone)\n")

    for i, game in enumerate(games, 1):
        # Show just the date, not the time (times can be confusing across timezones)
        date_str = game['date'].strftime('%a, %b %d, %Y')
        matchup = game['full_matchup']
        home_away = game['home_away']
        opponent = game['opponent']

        print(f"{i:2d}. {date_str}")
        print(f"    {matchup}")

        # Show if home or away
        if home_away == 'vs':
            print(f"    🏠 Home game vs {opponent}")
        else:
            print(f"    ✈️  Away game @ {opponent}")
        print()

    print("="*70)
    print("\n💡 To predict any of these games, use:")

    # Show first 3 upcoming games as examples
    for i, game in enumerate(games[:3], 1):
        if game['home_away'] == 'vs':
            # Home game
            print(f"   python3 predict_vegas.py \"{team_abbr}\" \"{game['opponent']}\"")
        else:
            # Away game
            print(f"   python3 predict_vegas.py \"{game['opponent']}\" \"{team_abbr}\"")

    print("="*70)


def main():
    """Main execution"""
    if len(sys.argv) >= 2:
        team_name = sys.argv[1]
        num_games = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
        display_schedule(team_name, num_games)
    else:
        print("\n📅 NBA Team Schedule Viewer")
        print("="*70)
        print("\nUsage: python3 get_schedule.py \"Team Name\" [num_games]")
        print("\nExamples:")
        print("  python3 get_schedule.py \"Lakers\"")
        print("  python3 get_schedule.py \"Lakers\" 5     # Next 5 games")
        print("  python3 get_schedule.py \"Celtics\" 15   # Next 15 games")
        print("\n📋 To see ALL available teams:")
        print("  python3 list_teams.py")
        print("\n💡 You can use:")
        print("  • Full name:  \"Los Angeles Lakers\"")
        print("  • Short name: \"Lakers\"")
        print("  • Abbreviation: \"LAL\"")
        print("\n✓ Uses ESPN's public API (FREE, no login required!)")
        print("="*70)


if __name__ == "__main__":
    main()

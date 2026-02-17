#!/usr/bin/env python3
"""
NBA Matchup Predictor - Using CURRENT stats.nba.com data
No API key required!
"""

import sys
from nba_stats_api import NBAStatsAPI

# Team abbreviation mapping
TEAM_ABBR_MAP = {
    'lakers': 'LAL', 'celtics': 'BOS', 'warriors': 'GSW', 'heat': 'MIA',
    'bucks': 'MIL', 'nuggets': 'DEN', 'suns': 'PHX', '76ers': 'PHI', 'sixers': 'PHI',
    'mavericks': 'DAL', 'mavs': 'DAL', 'clippers': 'LAC', 'grizzlies': 'MEM',
    'pelicans': 'NOP', 'blazers': 'POR', 'trail blazers': 'POR',
    'kings': 'SAC', 'spurs': 'SAS', 'thunder': 'OKC', 'jazz': 'UTA',
    'timberwolves': 'MIN', 'wolves': 'MIN', 'bulls': 'CHI', 'cavaliers': 'CLE',
    'cavs': 'CLE', 'hawks': 'ATL', 'hornets': 'CHA', 'magic': 'ORL',
    'pacers': 'IND', 'pistons': 'DET', 'raptors': 'TOR', 'wizards': 'WAS',
    'nets': 'BKN', 'knicks': 'NYK', 'rockets': 'HOU'
}

def get_team_abbr(team_name):
    """Convert team name to abbreviation"""
    team_lower = team_name.lower()

    # Check if it's already an abbreviation
    if len(team_name) == 3 and team_name.upper() in TEAM_ABBR_MAP.values():
        return team_name.upper()

    # Search in mapping
    for key, abbr in TEAM_ABBR_MAP.items():
        if key in team_lower:
            return abbr

    return None

def simple_predict(home_stats, visitor_stats):
    """
    Simple prediction based on stats

    Factors:
    - Points scored (offensive power): 40%
    - Points allowed (defensive power): 30%
    - Win rate (momentum): 30%
    """
    # Home team strength
    home_strength = (
        home_stats['avg_points_5'] * 0.4 +
        (120 - home_stats['avg_opp_points_5']) * 0.3 +
        home_stats['win_rate_5'] * 100 * 0.3
    )

    # Visitor team strength
    visitor_strength = (
        visitor_stats['avg_points_5'] * 0.4 +
        (120 - visitor_stats['avg_opp_points_5']) * 0.3 +
        visitor_stats['win_rate_5'] * 100 * 0.3
    )

    # Home court advantage (~3 points)
    home_strength += 3

    # Calculate probability
    total = home_strength + visitor_strength
    home_prob = home_strength / total if total > 0 else 0.5

    return {
        'prediction': 'Home Win' if home_prob > 0.5 else 'Visitor Win',
        'home_win_probability': home_prob,
        'visitor_win_probability': 1 - home_prob
    }

def predict_matchup(home_team, visitor_team):
    """Predict matchup between two teams"""
    print("\n" + "="*60)
    print("🏀 NBA MATCHUP PREDICTOR (CURRENT 2025-26 SEASON DATA)")
    print("="*60)
    print("\n📊 Using live data from stats.nba.com")
    print("   No API key required!")
    print()

    api = NBAStatsAPI()

    # Get team abbreviations
    home_abbr = get_team_abbr(home_team)
    visitor_abbr = get_team_abbr(visitor_team)

    if not home_abbr:
        print(f"❌ Unknown team: {home_team}")
        print("   Try: Lakers, Celtics, Warriors, Heat, etc.")
        return

    if not visitor_abbr:
        print(f"❌ Unknown team: {visitor_team}")
        print("   Try: Lakers, Celtics, Warriors, Heat, etc.")
        return

    print(f"Analyzing: {home_team} vs {visitor_team}")
    print("-"*60)

    # Get stats for both teams
    home_result = api.get_team_stats_last_n_games(home_abbr, n_games=5)
    if not home_result:
        print(f"❌ Could not fetch data for {home_team}")
        return

    home_stats, home_name, home_games = home_result

    visitor_result = api.get_team_stats_last_n_games(visitor_abbr, n_games=5)
    if not visitor_result:
        print(f"❌ Could not fetch data for {visitor_team}")
        return

    visitor_stats, visitor_name, visitor_games = visitor_result

    # Display stats
    print(f"\n{home_name} (Home) - Last 5 Games:")
    print(f"  Avg Points Scored: {home_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {home_stats['avg_opp_points_5']:.1f} (estimated)")
    print(f"  Win Rate: {home_stats['win_rate_5']:.1%}")
    wins = round(home_stats['win_rate_5'] * 5)
    losses = 5 - wins
    print(f"  Record: {wins}-{losses}")

    print(f"\nRecent games:")
    for game in home_games[:5]:
        date = game['GAME_DATE']
        matchup = game['MATCHUP']
        wl = game['WL']
        pts = game['PTS']
        print(f"  {date} | {matchup} | {wl} ({pts} pts)")

    print(f"\n{visitor_name} (Visitor) - Last 5 Games:")
    print(f"  Avg Points Scored: {visitor_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {visitor_stats['avg_opp_points_5']:.1f} (estimated)")
    print(f"  Win Rate: {visitor_stats['win_rate_5']:.1%}")
    wins = round(visitor_stats['win_rate_5'] * 5)
    losses = 5 - wins
    print(f"  Record: {wins}-{losses}")

    print(f"\nRecent games:")
    for game in visitor_games[:5]:
        date = game['GAME_DATE']
        matchup = game['MATCHUP']
        wl = game['WL']
        pts = game['PTS']
        print(f"  {date} | {matchup} | {wl} ({pts} pts)")

    # Make prediction
    prediction = simple_predict(home_stats, visitor_stats)

    print("\n" + "="*60)
    print("PREDICTION")
    print("="*60)

    print(f"\nMatchup: {home_name} (Home) vs {visitor_name} (Visitor)")
    print(f"\n🏆 Predicted Winner: {prediction['prediction']}")
    print(f"\n{home_name} Win Probability: {prediction['home_win_probability']:.1%}")
    print(f"{visitor_name} Win Probability: {prediction['visitor_win_probability']:.1%}")

    # Confidence level
    max_prob = max(prediction['home_win_probability'], prediction['visitor_win_probability'])
    if max_prob > 0.65:
        confidence = "HIGH"
    elif max_prob > 0.55:
        confidence = "MEDIUM"
    else:
        confidence = "TOSS-UP"

    print(f"\nConfidence: {confidence}")

    # Get data freshness
    if len(home_games) > 0:
        latest_date = home_games[0]['GAME_DATE']
        print(f"\n✓ Data is current (last game: {latest_date})")

    print("="*60)

def main():
    """Main execution"""
    if len(sys.argv) >= 3:
        home_team = sys.argv[1]
        visitor_team = sys.argv[2]
        predict_matchup(home_team, visitor_team)
    else:
        print("\n🏀 NBA Matchup Predictor")
        print("="*60)
        print("\nUsage: python3 predict_current.py \"Home Team\" \"Visitor Team\"")
        print("\nExamples:")
        print("  python3 predict_current.py \"Lakers\" \"Warriors\"")
        print("  python3 predict_current.py \"Celtics\" \"Heat\"")
        print("  python3 predict_current.py \"Bucks\" \"Suns\"")
        print("\n📋 To see ALL available teams:")
        print("  python3 list_teams.py")
        print("\n💡 You can use:")
        print("  • Full name:  \"Los Angeles Lakers\"")
        print("  • Short name: \"Lakers\"")
        print("  • Abbreviation: \"LAL\"")
        print("  • Nicknames: \"Sixers\", \"Mavs\", \"Wolves\", etc.")
        print("\n✓ Uses CURRENT data from stats.nba.com")
        print("✓ No API key required!")
        print("="*60)

if __name__ == "__main__":
    main()

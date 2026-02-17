#!/usr/bin/env python3
"""
Predict All Upcoming Games for a Team
Automatically fetches schedule and runs Vegas predictions
"""

import sys
from get_schedule import get_team_schedule, get_team_abbr, ESPN_TEAM_IDS
from predict_vegas import predict_matchup
from nba_stats_api import NBAStatsAPI

# Map ESPN abbreviations back to stats.nba.com abbreviations
ESPN_TO_NBA_MAP = {
    'GS': 'GSW',
    'NO': 'NOP',
    'NY': 'NYK',
    'SA': 'SAS',
    'WSH': 'WAS',
    'UTAH': 'UTA',
}


def convert_espn_abbr(espn_abbr):
    """Convert ESPN abbreviation to NBA Stats API abbreviation"""
    return ESPN_TO_NBA_MAP.get(espn_abbr, espn_abbr)


def predict_all_upcoming(team_name, num_games=5, show_details=False):
    """
    Predict all upcoming games for a team

    Args:
        team_name: Team name or abbreviation
        num_games: Number of upcoming games to predict
        show_details: If True, show full prediction details for each game
    """
    print("\n" + "="*80)
    print(f"🔮 PREDICT UPCOMING GAMES: {team_name}")
    print("="*80)

    # Get team abbreviation
    team_abbr = get_team_abbr(team_name)
    if not team_abbr:
        print(f"❌ Unknown team: {team_name}")
        print("   Try: Lakers, Celtics, Warriors, Heat, etc.")
        return

    # Convert to NBA Stats API abbreviation
    nba_abbr = convert_espn_abbr(team_abbr)

    print(f"\nFetching schedule for {team_abbr}...")

    # Get upcoming games
    games = get_team_schedule(team_abbr, num_games)

    if not games or len(games) == 0:
        print(f"❌ No upcoming games found for {team_name}")
        return

    print(f"✓ Found {len(games)} upcoming games\n")
    print("="*80)

    # Predict each game
    predictions = []

    for i, game in enumerate(games, 1):
        date_str = game['date'].strftime('%a, %b %d')
        opponent_espn = game['opponent']
        opponent_nba = convert_espn_abbr(opponent_espn)
        is_home = (game['home_away'] == 'vs')

        print(f"\n{'='*80}")
        print(f"GAME {i}/{len(games)}: {date_str} - {game['full_matchup']}")
        print(f"{'='*80}")

        if is_home:
            home_team = nba_abbr
            away_team = opponent_nba
        else:
            home_team = opponent_nba
            away_team = nba_abbr

        # Get quick prediction (without full details)
        from predict_vegas import vegas_predict
        from nba_stats_api import NBAStatsAPI
        from advanced_features import get_advanced_team_stats

        api = NBAStatsAPI()

        # Fetch stats for both teams
        home_result = api.get_team_stats_last_n_games(home_team, n_games=10)
        away_result = api.get_team_stats_last_n_games(away_team, n_games=10)

        if not home_result or not away_result:
            print(f"❌ Could not fetch data for this matchup")
            continue

        home_stats, home_name, home_games = home_result
        away_stats, away_name, away_games = away_result

        # Get prediction
        pred = vegas_predict(
            home_stats, away_stats,
            home_team, away_team,
            home_games, away_games
        )

        # Store prediction
        predictions.append({
            'game_num': i,
            'date': date_str,
            'matchup': game['full_matchup'],
            'is_home': is_home,
            'opponent': opponent_nba,
            'prediction': pred,
            'home_name': home_name,
            'away_name': away_name
        })

        # Display prediction
        if is_home:
            our_prob = pred['home_win_probability']
            opp_prob = pred['visitor_win_probability']
        else:
            our_prob = pred['visitor_win_probability']
            opp_prob = pred['home_win_probability']

        # Confidence
        max_prob = max(pred['home_win_probability'], pred['visitor_win_probability'])
        if max_prob > 0.70:
            confidence = "VERY HIGH 🔥"
        elif max_prob > 0.60:
            confidence = "HIGH ✓"
        elif max_prob > 0.55:
            confidence = "MEDIUM →"
        else:
            confidence = "TOSS-UP ⚖️"

        print(f"\n🏀 Matchup: {home_name} (Home) vs {away_name} (Away)")
        print(f"🎯 Predicted Winner: {pred['prediction']}")
        print(f"\n{nba_abbr} Win Probability: {our_prob:.1%}")
        print(f"{opponent_nba} Win Probability: {opp_prob:.1%}")
        print(f"\nConfidence: {confidence}")

        # Key stats
        adv = pred['advanced_stats']
        print(f"\n📊 Key Factors:")
        print(f"  Net Rating: {home_name} {adv['home_net_rating']:+.1f} vs "
              f"{away_name} {adv['visitor_net_rating']:+.1f}")
        print(f"  Travel: {adv['travel_distance']:.0f} miles "
              f"({adv['travel_fatigue']:.1f}% impact)")

    # Summary
    print("\n" + "="*80)
    print(f"📊 SUMMARY: {team_name}'s Next {len(predictions)} Games")
    print("="*80)

    wins = 0
    losses = 0

    for p in predictions:
        date = p['date']
        matchup = p['matchup']
        is_home = p['is_home']

        if is_home:
            our_prob = p['prediction']['home_win_probability']
        else:
            our_prob = p['prediction']['visitor_win_probability']

        will_win = our_prob > 0.5
        if will_win:
            wins += 1
            result = f"✓ WIN  ({our_prob:.0%})"
        else:
            losses += 1
            result = f"✗ LOSS ({our_prob:.0%})"

        location = "vs" if is_home else "@"
        print(f"{p['game_num']:2d}. {date:12s} {location} {p['opponent']:4s}  →  {result}")

    print("\n" + "="*80)
    print(f"📈 PREDICTED RECORD: {wins}-{losses}")

    if wins > losses:
        print(f"✓ Favorable stretch! Expected to win {wins}/{len(predictions)} games")
    elif wins < losses:
        print(f"⚠️  Tough stretch! Expected to win only {wins}/{len(predictions)} games")
    else:
        print(f"→ Even split expected ({wins}-{losses})")

    print("\n💡 These predictions use Vegas-level features:")
    print("   • Net Rating (most predictive stat)")
    print("   • Travel distance and fatigue")
    print("   • Rest differential")
    print("   • Target accuracy: 65-70%")
    print("="*80)


def main():
    """Main execution"""
    if len(sys.argv) >= 2:
        team_name = sys.argv[1]
        num_games = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
        predict_all_upcoming(team_name, num_games)
    else:
        print("\n🔮 Predict All Upcoming Games")
        print("="*80)
        print("\nUsage: python3 predict_upcoming.py \"Team Name\" [num_games]")
        print("\nExamples:")
        print("  python3 predict_upcoming.py \"Lakers\"")
        print("  python3 predict_upcoming.py \"Lakers\" 5      # Next 5 games")
        print("  python3 predict_upcoming.py \"Celtics\" 10    # Next 10 games")
        print("\n📋 To see ALL available teams:")
        print("  python3 list_teams.py")
        print("\n💡 This will:")
        print("  1. Fetch the team's upcoming schedule from ESPN")
        print("  2. Run Vegas-level predictions for each game")
        print("  3. Show predicted record for the stretch")
        print("\n✓ Uses Vegas-level predictions (65-70% accuracy)")
        print("="*80)


if __name__ == "__main__":
    main()

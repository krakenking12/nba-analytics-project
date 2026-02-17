#!/usr/bin/env python3
"""
NBA Matchup Predictor
Predict outcomes for any NBA matchup using real team statistics

Usage:
    python3 predict_matchup.py

Or specify teams directly:
    python3 predict_matchup.py "Lakers" "Warriors"
"""

import sys
import pandas as pd
from nba_analytics import NBAAnalytics


def list_teams(nba):
    """Display all available NBA teams"""
    print("\n" + "="*60)
    print("AVAILABLE NBA TEAMS")
    print("="*60)

    if nba.teams_data is None:
        nba.fetch_teams()

    teams = nba.teams_data.sort_values('full_name')

    print("\n{:<5} {:<30} {:<15}".format("ID", "Team", "City"))
    print("-" * 60)

    for _, team in teams.iterrows():
        print("{:<5} {:<30} {:<15}".format(
            team['id'],
            team['full_name'],
            team['city']
        ))

    print("\n")
    return teams


def get_team_recent_stats(nba, team_name, games_back=5):
    """
    Calculate recent performance stats for a team

    Args:
        nba: NBAAnalytics instance
        team_name: Name of the team to analyze
        games_back: Number of recent games to analyze (default: 5)
                   - 3 games: Very recent form (volatile)
                   - 5 games: Recent momentum (balanced) ✓ RECOMMENDED
                   - 10 games: Longer trend (more stable)
                   - 20 games: Season average (less responsive to recent changes)
    """
    if nba.teams_data is None:
        nba.fetch_teams()

    # Find team
    team = nba.teams_data[
        nba.teams_data['full_name'].str.contains(team_name, case=False) |
        nba.teams_data['name'].str.contains(team_name, case=False)
    ]

    if len(team) == 0:
        print(f"❌ Team '{team_name}' not found!")
        return None, None

    team = team.iloc[0]
    team_id = team['id']
    team_full_name = team['full_name']

    if nba.games_data is None or len(nba.games_data) == 0:
        print("⚠️  No games data available. Fetching now...")
        nba.fetch_games(seasons=['2024'], max_pages=10)

    # Get team's games
    home_games = nba.games_data[
        nba.games_data['home_team'].apply(lambda x: x['id'] if isinstance(x, dict) else None) == team_id
    ].copy()

    visitor_games = nba.games_data[
        nba.games_data['visitor_team'].apply(lambda x: x['id'] if isinstance(x, dict) else None) == team_id
    ].copy()

    # Process home games
    home_games['team_score'] = home_games['home_team_score']
    home_games['opp_score'] = home_games['visitor_team_score']
    home_games['won'] = (home_games['home_team_score'] > home_games['visitor_team_score']).astype(int)

    # Process visitor games
    visitor_games['team_score'] = visitor_games['visitor_team_score']
    visitor_games['opp_score'] = visitor_games['home_team_score']
    visitor_games['won'] = (visitor_games['visitor_team_score'] > visitor_games['home_team_score']).astype(int)

    # Combine all games
    all_games = pd.concat([
        home_games[['date', 'team_score', 'opp_score', 'won']],
        visitor_games[['date', 'team_score', 'opp_score', 'won']]
    ], ignore_index=True)

    # Remove games without scores (future games)
    all_games = all_games[all_games['team_score'].notna()].copy()

    # Sort by date (most recent first)
    all_games['date'] = all_games['date'].astype(str)
    all_games = all_games.sort_values('date', ascending=False)

    # Get last N games
    recent_games = all_games.head(games_back)

    if len(recent_games) == 0:
        print(f"❌ No recent games found for {team_full_name}")
        return None, None

    # Calculate stats
    stats = {
        'avg_points_5': recent_games['team_score'].mean(),
        'avg_opp_points_5': recent_games['opp_score'].mean(),
        'win_rate_5': recent_games['won'].mean()
    }

    return stats, team_full_name


def predict_matchup_interactive(nba):
    """Interactive matchup prediction"""
    print("\n" + "="*60)
    print("NBA MATCHUP PREDICTOR")
    print("="*60)

    # Show available teams
    teams = list_teams(nba)

    # Get home team
    print("Enter HOME team name (or partial name):")
    home_team_input = input("Home Team: ").strip()

    # Get visitor team
    print("\nEnter VISITOR team name (or partial name):")
    visitor_team_input = input("Visitor Team: ").strip()

    print("\n" + "-"*60)
    print("Analyzing matchup...")
    print("-"*60)

    # Get stats
    home_stats, home_name = get_team_recent_stats(nba, home_team_input)
    visitor_stats, visitor_name = get_team_recent_stats(nba, visitor_team_input)

    if home_stats is None or visitor_stats is None:
        print("\n❌ Could not retrieve team stats. Please try again.")
        return

    # Display stats
    print(f"\n{home_name} (Home) - Last 5 Games:")
    print(f"  Avg Points Scored: {home_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {home_stats['avg_opp_points_5']:.1f}")
    print(f"  Win Rate: {home_stats['win_rate_5']:.1%}")

    print(f"\n{visitor_name} (Visitor) - Last 5 Games:")
    print(f"  Avg Points Scored: {visitor_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {visitor_stats['avg_opp_points_5']:.1f}")
    print(f"  Win Rate: {visitor_stats['win_rate_5']:.1%}")

    # Make prediction
    print("\n" + "="*60)
    print("PREDICTION")
    print("="*60)

    if nba.model is None:
        print("\n⚠️  Model not trained yet. Training now...")
        if nba.stats_data is None:
            nba.engineer_features()
        nba.train_model()

    prediction = nba.predict_game(home_stats, visitor_stats)

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
    print("="*60)


def predict_matchup_direct(nba, home_team, visitor_team):
    """Predict matchup with team names provided as arguments"""
    print("\n" + "="*60)
    print("NBA MATCHUP PREDICTOR")
    print("="*60)

    print(f"\nAnalyzing: {home_team} (Home) vs {visitor_team} (Visitor)")
    print("-"*60)

    # Get stats
    home_stats, home_name = get_team_recent_stats(nba, home_team)
    visitor_stats, visitor_name = get_team_recent_stats(nba, visitor_team)

    if home_stats is None or visitor_stats is None:
        print("\n❌ Could not retrieve team stats.")
        return

    # Display stats
    print(f"\n{home_name} (Home) - Last 5 Games:")
    print(f"  Avg Points Scored: {home_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {home_stats['avg_opp_points_5']:.1f}")
    print(f"  Win Rate: {home_stats['win_rate_5']:.1%}")

    print(f"\n{visitor_name} (Visitor) - Last 5 Games:")
    print(f"  Avg Points Scored: {visitor_stats['avg_points_5']:.1f}")
    print(f"  Avg Points Allowed: {visitor_stats['avg_opp_points_5']:.1f}")
    print(f"  Win Rate: {visitor_stats['win_rate_5']:.1%}")

    # Make prediction
    print("\n" + "="*60)
    print("PREDICTION")
    print("="*60)

    if nba.model is None:
        print("\n⚠️  Model not trained yet. Training now...")
        if nba.stats_data is None:
            nba.engineer_features()
        nba.train_model()

    prediction = nba.predict_game(home_stats, visitor_stats)

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
    print("="*60)


def main():
    """Main execution"""
    print("\n🏀 NBA Matchup Predictor")
    print("="*60)

    # Initialize
    nba = NBAAnalytics()

    # Fetch data
    print("\n📊 Loading NBA data...")
    print("(This may take a minute on first run)")
    print("-"*60)

    nba.fetch_teams()

    print("Fetching 2025-2026 season games (current season only)...")
    nba.fetch_games(seasons=['2025'], max_pages=10)

    if nba.games_data is None or len(nba.games_data) == 0:
        print("\n❌ ERROR: No 2025-2026 season data available from API.")
        print("   This could mean:")
        print("   1. The season hasn't started yet")
        print("   2. API is down or rate limited")
        print("   3. API key is invalid")
        print("\n   Try running: python3 demo.py (for sample data)")
        return

    print(f"✓ Loaded {len(nba.games_data)} games")

    # Engineer features and train model
    print("\n🔧 Preparing prediction model...")
    nba.engineer_features()
    nba.train_model()

    # Check if teams provided as arguments
    if len(sys.argv) == 3:
        home_team = sys.argv[1]
        visitor_team = sys.argv[2]
        predict_matchup_direct(nba, home_team, visitor_team)
    else:
        # Interactive mode
        predict_matchup_interactive(nba)

        # Ask if they want to predict another
        while True:
            print("\n" + "-"*60)
            response = input("\nPredict another matchup? (y/n): ").strip().lower()
            if response == 'y' or response == 'yes':
                predict_matchup_interactive(nba)
            else:
                break

    print("\n✅ Done! Thanks for using NBA Matchup Predictor!")
    print()


if __name__ == "__main__":
    main()

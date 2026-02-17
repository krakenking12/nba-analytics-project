#!/usr/bin/env python3
"""
NBA Analytics Demo - Simplified Version
This version uses sample data to demonstrate the concept
"""

import json
import random
from datetime import datetime, timedelta

# Sample NBA teams
TEAMS = {
    1: "Lakers", 2: "Warriors", 3: "Celtics", 4: "Heat",
    5: "Bucks", 6: "Nuggets", 7: "Suns", 8: "76ers",
    9: "Mavericks", 10: "Clippers"
}

def generate_sample_games(num_games=100):
    """Generate sample game data for demonstration"""
    games = []
    start_date = datetime(2024, 10, 1)
    
    for i in range(num_games):
        home_team = random.randint(1, 10)
        visitor_team = random.randint(1, 10)
        while visitor_team == home_team:
            visitor_team = random.randint(1, 10)
        
        # Simulate scores with home court advantage
        home_base = random.randint(95, 115)
        visitor_base = random.randint(95, 115)
        
        # Home court advantage (~3 points)
        home_score = home_base + random.randint(0, 5)
        visitor_score = visitor_base
        
        game = {
            'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
            'home_team_id': home_team,
            'visitor_team_id': visitor_team,
            'home_score': home_score,
            'visitor_score': visitor_score,
            'home_win': 1 if home_score > visitor_score else 0
        }
        games.append(game)
    
    return games

def calculate_team_stats(games, team_id):
    """Calculate rolling stats for a team"""
    team_games = []
    
    for game in games:
        if game['home_team_id'] == team_id:
            team_games.append({
                'date': game['date'],
                'score': game['home_score'],
                'opp_score': game['visitor_score'],
                'won': game['home_win']
            })
        elif game['visitor_team_id'] == team_id:
            team_games.append({
                'date': game['date'],
                'score': game['visitor_score'],
                'opp_score': game['home_score'],
                'won': 0 if game['home_win'] else 1
            })
    
    # Sort by date
    team_games.sort(key=lambda x: x['date'])
    
    # Calculate rolling averages (last 5 games)
    stats = []
    for i in range(len(team_games)):
        start_idx = max(0, i - 4)
        recent_games = team_games[start_idx:i+1]
        
        avg_points = sum(g['score'] for g in recent_games) / len(recent_games)
        avg_opp_points = sum(g['opp_score'] for g in recent_games) / len(recent_games)
        win_rate = sum(g['won'] for g in recent_games) / len(recent_games)
        
        stats.append({
            'date': team_games[i]['date'],
            'avg_points_5': avg_points,
            'avg_opp_points_5': avg_opp_points,
            'win_rate_5': win_rate
        })
    
    return stats

def simple_predict(home_stats, visitor_stats):
    """Simple prediction based on stats"""
    # Calculate strength score
    home_strength = (
        home_stats['avg_points_5'] * 0.4 +
        (120 - home_stats['avg_opp_points_5']) * 0.3 +
        home_stats['win_rate_5'] * 100 * 0.3
    )
    
    visitor_strength = (
        visitor_stats['avg_points_5'] * 0.4 +
        (120 - visitor_stats['avg_opp_points_5']) * 0.3 +
        visitor_stats['win_rate_5'] * 100 * 0.3
    )
    
    # Add home court advantage
    home_strength += 3
    
    # Calculate probability
    total = home_strength + visitor_strength
    home_prob = home_strength / total
    
    return {
        'prediction': 'Home Win' if home_prob > 0.5 else 'Visitor Win',
        'home_win_probability': home_prob,
        'visitor_win_probability': 1 - home_prob
    }

def main():
    print("="*60)
    print("⚠️  NBA ANALYTICS DEMO - SAMPLE DATA ONLY")
    print("="*60)
    print()
    print("WARNING: This demo uses RANDOMLY GENERATED data!")
    print("         This is NOT real NBA statistics.")
    print("         For REAL predictions, use predict_matchup.py")
    print()
    print("="*60)
    print()

    # Generate sample data
    print("Generating SAMPLE game data (not real!)...")
    games = generate_sample_games(100)
    print(f"✓ Generated {len(games)} SAMPLE games")
    print()
    
    # Calculate stats for each team
    print("Calculating team statistics...")
    team_stats = {}
    for team_id in TEAMS.keys():
        team_stats[team_id] = calculate_team_stats(games, team_id)
    print(f"✓ Calculated stats for {len(TEAMS)} teams")
    print()
    
    # Analyze overall trends
    print("OVERALL STATISTICS")
    print("-" * 60)
    home_wins = sum(g['home_win'] for g in games)
    home_win_rate = home_wins / len(games)
    avg_total_points = sum(g['home_score'] + g['visitor_score'] for g in games) / len(games)
    
    print(f"Total Games: {len(games)}")
    print(f"Home Win Rate: {home_win_rate:.1%}")
    print(f"Average Total Points: {avg_total_points:.1f}")
    print()
    
    # Team performance summary
    print("TOP PERFORMING TEAMS (by avg points)")
    print("-" * 60)
    
    team_avg_points = {}
    for team_id, stats in team_stats.items():
        if stats:
            avg = sum(s['avg_points_5'] for s in stats) / len(stats)
            team_avg_points[team_id] = avg
    
    sorted_teams = sorted(team_avg_points.items(), key=lambda x: x[1], reverse=True)
    for i, (team_id, avg_pts) in enumerate(sorted_teams[:5], 1):
        print(f"{i}. {TEAMS[team_id]}: {avg_pts:.1f} ppg")
    print()
    
    # Example prediction
    print("EXAMPLE PREDICTION")
    print("-" * 60)
    
    # Lakers vs Warriors example
    lakers_id = 1
    warriors_id = 2
    
    # Get most recent stats
    lakers_recent = team_stats[lakers_id][-1] if team_stats[lakers_id] else None
    warriors_recent = team_stats[warriors_id][-1] if team_stats[warriors_id] else None
    
    if lakers_recent and warriors_recent:
        print(f"\nMatchup: {TEAMS[lakers_id]} (Home) vs {TEAMS[warriors_id]} (Visitor)")
        print()
        print(f"{TEAMS[lakers_id]} Stats (Last 5 Games):")
        print(f"  Avg Points: {lakers_recent['avg_points_5']:.1f}")
        print(f"  Avg Opp Points: {lakers_recent['avg_opp_points_5']:.1f}")
        print(f"  Win Rate: {lakers_recent['win_rate_5']:.1%}")
        print()
        print(f"{TEAMS[warriors_id]} Stats (Last 5 Games):")
        print(f"  Avg Points: {warriors_recent['avg_points_5']:.1f}")
        print(f"  Avg Opp Points: {warriors_recent['avg_opp_points_5']:.1f}")
        print(f"  Win Rate: {warriors_recent['win_rate_5']:.1%}")
        print()
        
        prediction = simple_predict(lakers_recent, warriors_recent)
        print("PREDICTION:")
        print(f"  Winner: {prediction['prediction']}")
        print(f"  {TEAMS[lakers_id]} Win Probability: {prediction['home_win_probability']:.1%}")
        print(f"  {TEAMS[warriors_id]} Win Probability: {prediction['visitor_win_probability']:.1%}")
    
    print()
    print("="*60)
    print("PROJECT INSIGHTS")
    print("="*60)
    print()
    print("This demo showcases:")
    print("✓ Data pipeline development")
    print("✓ Feature engineering (rolling averages)")
    print("✓ Statistical analysis")
    print("✓ Predictive modeling")
    print("✓ Business insights generation")
    print()
    print("Full version would include:")
    print("• Real NBA API integration")
    print("• Machine learning models (Random Forest, XGBoost)")
    print("• Advanced visualizations")
    print("• Model evaluation metrics")
    print("• Interactive dashboard")
    print()
    print("="*60)

if __name__ == "__main__":
    main()

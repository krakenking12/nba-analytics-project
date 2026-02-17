#!/usr/bin/env python3
"""
NBA Vegas-Level Predictor WITH Injury Tracking
Enhanced version with star player injury impact
"""

import sys
import math
from injury_data import InjuryTracker, STAR_PLAYER_IMPACT

# Import existing functionality (you'll need to adapt this to your actual predict_vegas.py structure)
# For now, I'll create a simplified version

# Team locations for Haversine distance calculation
TEAM_LOCATIONS = {
    'LAL': (34.0430, -118.2673),  # Los Angeles
    'LAC': (34.0430, -118.2673),
    'BOS': (42.3662, -71.0621),   # Boston
    'GS': (37.7680, -122.3877),   # San Francisco
    'MIA': (25.7814, -80.1870),   # Miami
    'PHX': (33.4457, -112.0712),  # Phoenix
    'PHI': (39.9012, -75.1720),   # Philadelphia
    'DAL': (32.7905, -96.8103),   # Dallas
    'MIL': (43.0436, -87.9170),   # Milwaukee
    'DEN': (39.7487, -105.0077),  # Denver
    'NY': (40.7505, -73.9934),    # New York
    'BKN': (40.6853, -73.9742),   # Brooklyn
    'TOR': (43.6435, -79.3791),   # Toronto
    'CHI': (41.8807, -87.6742),   # Chicago
    'CLE': (41.4965, -81.6882),   # Cleveland
    'ATL': (33.7573, -84.3963),   # Atlanta
    'CHA': (35.2251, -80.8392),   # Charlotte
    'ORL': (28.5392, -81.3839),   # Orlando
    'IND': (39.7640, -86.1555),   # Indianapolis
    'DET': (42.3410, -83.0550),   # Detroit
    'WSH': (38.8981, -77.0209),   # Washington
    'MEM': (35.1382, -90.0505),   # Memphis
    'NO': (29.9490, -90.0821),    # New Orleans
    'SA': (29.4271, -98.4375),    # San Antonio
    'HOU': (29.7508, -95.3621),   # Houston
    'OKC': (35.4634, -97.5151),   # Oklahoma City
    'MIN': (44.9795, -93.2760),   # Minneapolis
    'POR': (45.5316, -122.6668),  # Portland
    'UTAH': (40.7683, -111.9011), # Salt Lake City
    'SAC': (38.5803, -121.4996),  # Sacramento
}


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points on Earth using Haversine formula

    Returns distance in miles
    """
    R = 3958.8  # Earth radius in miles

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def calculate_travel_fatigue(away_team, home_team):
    """
    Calculate travel fatigue impact for away team

    Returns negative adjustment to win probability
    """
    if away_team not in TEAM_LOCATIONS or home_team not in TEAM_LOCATIONS:
        return 0

    away_loc = TEAM_LOCATIONS[away_team]
    home_loc = TEAM_LOCATIONS[home_team]

    distance = haversine_distance(away_loc[0], away_loc[1], home_loc[0], home_loc[1])

    # Travel fatigue impact based on distance
    if distance < 500:
        return -0.005  # -0.5%
    elif distance < 1500:
        return -0.020  # -2.0%
    elif distance < 2500:
        return -0.050  # -5.0%
    else:
        return -0.070  # -7.0% (coast-to-coast)


def predict_with_injuries(home_team, away_team, injury_tracker=None):
    """
    Predict game outcome with injury adjustments

    Args:
        home_team: Home team abbreviation
        away_team: Away team abbreviation
        injury_tracker: InjuryTracker instance (optional)

    Returns:
        Dictionary with prediction results
    """

    print(f"\n{'='*70}")
    print(f"🎯 PREDICTING: {home_team} vs {away_team}")
    print(f"{'='*70}")

    # STEP 1: Base prediction (simplified - replace with your actual XGBoost model)
    # For now, using simplified heuristics
    base_home_advantage = 0.035  # 3.5% home court advantage

    # Calculate travel fatigue
    travel_impact = calculate_travel_fatigue(away_team, home_team)

    # Base probability before injuries
    base_home_win_prob = 0.50 + base_home_advantage + abs(travel_impact)

    print(f"\n📊 BASE PREDICTION (before injuries):")
    print(f"   Home advantage: +3.5%")
    print(f"   Travel fatigue: {travel_impact*100:.1f}%")
    print(f"   Base home win prob: {base_home_win_prob*100:.1f}%")

    # STEP 2: Adjust for injuries
    if injury_tracker:
        adjusted_prob = injury_tracker.adjust_prediction_for_injuries(
            home_team, away_team, base_home_win_prob
        )
    else:
        adjusted_prob = base_home_win_prob
        print("\n⚠️  No injury data provided - using base prediction")

    # STEP 3: Calculate final probabilities
    home_win_prob = adjusted_prob
    away_win_prob = 1 - adjusted_prob

    print(f"\n🎯 FINAL PREDICTION (with injuries):")
    print(f"   {home_team} win probability: {home_win_prob*100:.1f}%")
    print(f"   {away_team} win probability: {away_win_prob*100:.1f}%")

    # Determine confidence level
    diff = abs(home_win_prob - 0.5)
    if diff < 0.05:
        confidence = "TOSS-UP ⚖️"
    elif diff < 0.10:
        confidence = "MEDIUM →"
    elif diff < 0.20:
        confidence = "HIGH ✓"
    else:
        confidence = "VERY HIGH 🔥"

    print(f"   Confidence: {confidence}")

    # Determine predicted winner
    if home_win_prob > 0.5:
        predicted_winner = home_team
        winner_prob = home_win_prob
    else:
        predicted_winner = away_team
        winner_prob = away_win_prob

    print(f"\n✅ PREDICTED WINNER: {predicted_winner} ({winner_prob*100:.1f}%)")
    print(f"{'='*70}\n")

    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_win_prob': home_win_prob,
        'away_win_prob': away_win_prob,
        'predicted_winner': predicted_winner,
        'confidence': confidence,
        'travel_impact': travel_impact,
        'base_prob': base_home_win_prob,
        'injury_adjusted_prob': adjusted_prob
    }


def main():
    """Main execution"""

    if len(sys.argv) < 3:
        print("\n🎯 NBA Game Predictor WITH INJURY TRACKING")
        print("="*70)
        print("\nUsage: python3 predict_vegas_with_injuries.py <home_team> <away_team>")
        print("\nExamples:")
        print('  python3 predict_vegas_with_injuries.py "Lakers" "Celtics"')
        print('  python3 predict_vegas_with_injuries.py "LAL" "BOS"')
        print("\n💡 Make sure injuries.csv file exists with current injury data")
        print("="*70)
        return

    home_team = sys.argv[1].upper()
    away_team = sys.argv[2].upper()

    # Load injury tracker
    print("\n🏥 Loading injury data...")
    injury_tracker = InjuryTracker("injuries.csv")

    # Make prediction
    result = predict_with_injuries(home_team, away_team, injury_tracker)

    print("\n💡 TIP: Update injuries.csv to get accurate predictions!")
    print("   Each injury can swing predictions by 4-26% (2-13 points)")


if __name__ == "__main__":
    main()

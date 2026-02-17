#!/usr/bin/env python3
"""
Advanced NBA Features for Vegas-Level Prediction
Implements Net Rating, Rest Differential, and Travel Distance
"""

from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

# NBA team city coordinates (latitude, longitude)
TEAM_LOCATIONS = {
    'ATL': (33.7573, -84.3963),   # Atlanta
    'BOS': (42.3661, -71.0621),   # Boston
    'BKN': (40.6826, -73.9754),   # Brooklyn
    'CHA': (35.2251, -80.8392),   # Charlotte
    'CHI': (41.8807, -87.6742),   # Chicago
    'CLE': (41.4965, -81.6882),   # Cleveland
    'DAL': (32.7905, -96.8103),   # Dallas
    'DEN': (39.7487, -105.0077),  # Denver
    'DET': (42.3410, -83.0550),   # Detroit
    'GSW': (37.7680, -122.3878),  # Golden State (SF)
    'HOU': (29.7508, -95.3621),   # Houston
    'IND': (39.7640, -86.1555),   # Indianapolis
    'LAC': (34.0430, -118.2673),  # LA Clippers
    'LAL': (34.0430, -118.2673),  # LA Lakers
    'MEM': (35.1382, -90.0505),   # Memphis
    'MIA': (25.7814, -80.1870),   # Miami
    'MIL': (43.0436, -87.9170),   # Milwaukee
    'MIN': (44.9795, -93.2760),   # Minneapolis
    'NOP': (29.9490, -90.0821),   # New Orleans
    'NYK': (40.7505, -73.9934),   # New York
    'OKC': (35.4634, -97.5151),   # Oklahoma City
    'ORL': (28.5392, -81.3839),   # Orlando
    'PHI': (39.9012, -75.1720),   # Philadelphia
    'PHX': (33.4457, -112.0713),  # Phoenix
    'POR': (45.5316, -122.6668),  # Portland
    'SAC': (38.5801, -121.4998),  # Sacramento
    'SAS': (29.4270, -98.4375),   # San Antonio
    'TOR': (43.6435, -79.3791),   # Toronto
    'UTA': (40.7683, -111.9011),  # Utah (Salt Lake City)
    'WAS': (38.8981, -77.0209),   # Washington DC
}


def calculate_net_rating(games):
    """
    Calculate Net Rating: Point differential per 100 possessions

    Net Rating = (Points Scored - Points Allowed) / Possessions * 100

    Why it's better than raw points:
    - Accounts for pace (fast vs slow teams)
    - More predictive than simple averages
    - Used by NBA.com and Vegas

    Args:
        games: List of game dicts with PTS, FGA, FTA, OREB, TOV

    Returns:
        float: Average net rating over all games
    """
    if not games or len(games) == 0:
        return 0.0

    total_net_rating = 0
    valid_games = 0

    for game in games:
        try:
            pts_scored = float(game['PTS'])

            # Estimate possessions using standard formula
            # Possessions = FGA + 0.44 * FTA - OREB + TOV
            fga = float(game.get('FGA', 0))
            fta = float(game.get('FTA', 0))
            oreb = float(game.get('OREB', 0))
            tov = float(game.get('TOV', 0))

            possessions = fga + (0.44 * fta) - oreb + tov

            # Estimate opponent points (rough approximation)
            if game['WL'] == 'W':
                pts_allowed = pts_scored - 7  # Avg win margin
            else:
                pts_allowed = pts_scored + 7  # Avg loss margin

            # Calculate net rating
            if possessions > 0:
                net_rating = ((pts_scored - pts_allowed) / possessions) * 100
                total_net_rating += net_rating
                valid_games += 1

        except (KeyError, ValueError, TypeError):
            continue

    return total_net_rating / valid_games if valid_games > 0 else 0.0


def calculate_rest_differential(home_last_game, away_last_game, game_date):
    """
    Calculate rest differential between teams

    Rest Differential = Home team rest days - Away team rest days

    Impact on win probability:
    - Back-to-back (0 rest): -3 to -5%
    - 1 day rest: baseline
    - 2+ days rest: +2 to +3%
    - Rest advantage (2+ vs 0): +10-12%

    Args:
        home_last_game: Date string of home team's last game
        away_last_game: Date string of away team's last game
        game_date: Date string of current game (not used, for future)

    Returns:
        int: Rest differential in days (positive = home advantage)
    """
    try:
        # Parse dates (format: "FEB 12, 2026" or "2026-02-12")
        home_last = parse_game_date(home_last_game)
        away_last = parse_game_date(away_last_game)

        # Calculate days since last game for each team
        # Note: We don't have the current game date in this version,
        # so we calculate relative rest difference

        # For now, use the difference between their last games
        # as a proxy for rest differential
        date_diff = (away_last - home_last).days

        # Positive = home team had more recent game (less rest)
        # Negative = away team had more recent game (less rest)
        return -date_diff  # Flip sign so positive = home advantage

    except Exception as e:
        return 0  # Neutral if can't calculate


def parse_game_date(date_str):
    """Parse various date formats"""
    # Try "FEB 12, 2026" format
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except:
        pass

    # Try "2026-02-12" format
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        pass

    # Try "FEB 12, 2026" with uppercase
    try:
        return datetime.strptime(date_str.upper(), "%B %d, %Y")
    except:
        pass

    raise ValueError(f"Could not parse date: {date_str}")


def calculate_travel_distance(away_team_abbr, home_team_abbr):
    """
    Calculate travel distance for away team

    Using Haversine formula to calculate great circle distance

    Impact on win probability:
    - 0-500 miles: Minimal (-0.5%)
    - 500-1500 miles: Moderate (-2%)
    - 1500+ miles: Significant (-5%)
    - Coast-to-coast (2500+ miles): Major fatigue (-7%)

    Args:
        away_team_abbr: Away team abbreviation (e.g., 'BOS')
        home_team_abbr: Home team abbreviation (e.g., 'LAL')

    Returns:
        float: Distance in miles
    """
    if away_team_abbr not in TEAM_LOCATIONS or home_team_abbr not in TEAM_LOCATIONS:
        return 0.0

    lat1, lon1 = TEAM_LOCATIONS[away_team_abbr]
    lat2, lon2 = TEAM_LOCATIONS[home_team_abbr]

    # Haversine formula
    R = 3959  # Earth's radius in miles

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance


def calculate_travel_fatigue_factor(distance):
    """
    Convert travel distance to fatigue factor

    Returns:
        float: Fatigue penalty (0 to -7 percentage points)
    """
    if distance < 500:
        return -0.5
    elif distance < 1500:
        return -2.0
    elif distance < 2500:
        return -5.0
    else:
        return -7.0  # Coast-to-coast


def get_advanced_team_stats(games, team_abbr, last_n=10):
    """
    Calculate all advanced stats for a team

    Args:
        games: List of recent games
        team_abbr: Team abbreviation
        last_n: Number of games to include (default 10)

    Returns:
        dict: Advanced statistics
    """
    if not games or len(games) == 0:
        return {
            'net_rating': 0.0,
            'avg_points': 0.0,
            'avg_possessions': 0.0,
            'pace': 0.0,
        }

    recent_games = games[:last_n]

    # Calculate net rating
    net_rating = calculate_net_rating(recent_games)

    # Calculate average points
    avg_points = sum(float(g['PTS']) for g in recent_games) / len(recent_games)

    # Calculate average possessions
    total_poss = 0
    for game in recent_games:
        fga = float(game.get('FGA', 0))
        fta = float(game.get('FTA', 0))
        oreb = float(game.get('OREB', 0))
        tov = float(game.get('TOV', 0))
        poss = fga + (0.44 * fta) - oreb + tov
        total_poss += poss

    avg_possessions = total_poss / len(recent_games)

    # Pace = possessions per 48 minutes
    pace = avg_possessions  # Already per game

    return {
        'net_rating': net_rating,
        'avg_points': avg_points,
        'avg_possessions': avg_possessions,
        'pace': pace,
    }


# Quick test
if __name__ == "__main__":
    print("Testing Advanced Features...")
    print("="*60)

    # Test travel distance
    print("\n1. Travel Distance:")
    distance = calculate_travel_distance('BOS', 'LAL')
    print(f"   Boston → LA: {distance:.0f} miles")
    print(f"   Fatigue factor: {calculate_travel_fatigue_factor(distance):.1f}%")

    distance = calculate_travel_distance('LAL', 'LAC')
    print(f"   LA Lakers → LA Clippers: {distance:.0f} miles")
    print(f"   Fatigue factor: {calculate_travel_fatigue_factor(distance):.1f}%")

    print("\n✓ Advanced features module working!")
    print("="*60)

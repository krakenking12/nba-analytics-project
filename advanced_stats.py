#!/usr/bin/env python3
"""
Advanced NBA Statistics Calculator
Calculates Net Rating, Offensive/Defensive Rating, Pace from game data
"""

import time
from nba_api.stats.endpoints import teamgamelog

ABBREV_ALIASES = {
    'GSW': 'GS', 'NOP': 'NO', 'NYK': 'NY',
    'SAS': 'SA', 'UTA': 'UTAH', 'WAS': 'WSH',
}

# Team IDs
NBA_TEAM_IDS = {
    'ATL': 1610612737, 'BOS': 1610612738, 'BKN': 1610612751, 'CHA': 1610612766,
    'CHI': 1610612741, 'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743,
    'DET': 1610612765, 'GS': 1610612744, 'HOU': 1610612745, 'IND': 1610612754,
    'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763, 'MIA': 1610612748,
    'MIL': 1610612749, 'MIN': 1610612750, 'NO': 1610612740, 'NY': 1610612752,
    'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756,
    'POR': 1610612757, 'SAC': 1610612758, 'SA': 1610612759, 'TOR': 1610612761,
    'UTAH': 1610612762, 'WSH': 1610612764
}


def calculate_possessions(fga, fta, oreb, tov):
    """
    Calculate possessions using standard NBA formula

    Possessions = FGA + 0.44*FTA - OREB + TOV

    Args:
        fga: Field goal attempts
        fta: Free throw attempts
        oreb: Offensive rebounds
        tov: Turnovers

    Returns:
        Estimated possessions
    """
    return fga + (0.44 * fta) - oreb + tov


def calculate_offensive_rating(pts, possessions):
    """
    Calculate offensive rating (points per 100 possessions)

    Args:
        pts: Points scored
        possessions: Team possessions

    Returns:
        Offensive rating (pts per 100 possessions)
    """
    if possessions == 0:
        return 0
    return (pts / possessions) * 100


def calculate_defensive_rating(opp_pts, possessions):
    """
    Calculate defensive rating (points allowed per 100 possessions)

    Args:
        opp_pts: Opponent points
        possessions: Team possessions

    Returns:
        Defensive rating (pts allowed per 100 possessions)
    """
    if possessions == 0:
        return 0
    return (opp_pts / possessions) * 100


def calculate_net_rating(off_rating, def_rating):
    """
    Calculate net rating (offensive rating - defensive rating)

    Positive = team scores more than they allow (good)
    Negative = team allows more than they score (bad)

    Args:
        off_rating: Offensive rating
        def_rating: Defensive rating

    Returns:
        Net rating
    """
    return off_rating - def_rating


def fetch_team_game_stats(team_abbr, season="2025-26", max_games=82):
    """
    Fetch detailed game stats for a team using nba_api

    Args:
        team_abbr: Team abbreviation
        season: Season (e.g., '2025-26', '2023-24')
        max_games: Maximum games to fetch

    Returns:
        List of games with detailed stats
    """
    team_id = NBA_TEAM_IDS.get(team_abbr)
    if not team_id:
        return []

    try:
        time.sleep(0.6)  # Respect rate limits
        log = teamgamelog.TeamGameLog(
            team_id=team_id,
            season=season,
            season_type_all_star='Regular Season'
        )
        df = log.get_data_frames()[0]

        games = []

        for _, row in df.head(max_games).iterrows():
            pts = row['PTS']
            fga = row['FGA']
            fta = row['FTA']
            oreb = row['OREB']
            tov = row['TOV']
            matchup = row['MATCHUP']
            wl = row['WL']

            is_home = ' vs. ' in matchup

            if ' vs. ' in matchup:
                opponent = matchup.split(' vs. ')[1]
            elif ' @ ' in matchup:
                opponent = matchup.split(' @ ')[1]
            else:
                opponent = 'UNK'

            opponent = ABBREV_ALIASES.get(opponent, opponent)

            possessions = calculate_possessions(fga, fta, oreb, tov)
            off_rating = calculate_offensive_rating(pts, possessions)

            games.append({
                'team': team_abbr,
                'opponent': opponent,
                'is_home': is_home,
                'won': (wl == 'W'),
                'pts': pts,
                'fga': fga,
                'fta': fta,
                'oreb': oreb,
                'tov': tov,
                'possessions': possessions,
                'off_rating': off_rating,
                'game_date': row['GAME_DATE'],
                'matchup': matchup
            })

        return games

    except Exception as e:
        print(f"Error fetching stats for {team_abbr}: {e}")
        return []


def calculate_team_average_stats(games, last_n_games=10):
    """
    Calculate average statistics over last N games

    Args:
        games: List of game dictionaries
        last_n_games: Number of recent games to average

    Returns:
        Dictionary of average stats
    """
    if not games:
        return {
            'avg_pts': 0,
            'avg_off_rating': 100,
            'avg_possessions': 100,
            'win_pct': 0.5,
        }

    recent_games = games[:last_n_games]

    total_pts = sum(g['pts'] for g in recent_games)
    total_off_rating = sum(g['off_rating'] for g in recent_games)
    total_possessions = sum(g['possessions'] for g in recent_games)
    wins = sum(1 for g in recent_games if g['won'])

    n = len(recent_games)

    return {
        'avg_pts': total_pts / n if n > 0 else 0,
        'avg_off_rating': total_off_rating / n if n > 0 else 100,
        'avg_possessions': total_possessions / n if n > 0 else 100,
        'win_pct': wins / n if n > 0 else 0.5,
        'num_games': n
    }


def get_team_net_rating(team_abbr, season="2023-24", last_n_games=10):
    """
    Get team's Net Rating based on recent games

    This is a simplified version - real Net Rating requires opponent stats too

    Args:
        team_abbr: Team abbreviation
        season: Season
        last_n_games: Number of recent games to consider

    Returns:
        Approximate Net Rating
    """
    games = fetch_team_game_stats(team_abbr, season, max_games=last_n_games)

    if not games:
        return 0.0  # Neutral if no data

    stats = calculate_team_average_stats(games, last_n_games)

    # Simplified Net Rating approximation
    # Real calculation requires opponent offensive rating
    # We'll estimate based on win percentage and offensive rating

    # Average NBA offensive rating is around 110-115
    # If team scores well above average, they likely have positive net rating
    avg_nba_rating = 112

    estimated_net_rating = stats['avg_off_rating'] - avg_nba_rating

    # Adjust based on win percentage
    win_adjustment = (stats['win_pct'] - 0.5) * 10  # Scale win% to rating points

    net_rating = estimated_net_rating + win_adjustment

    return net_rating


def test_advanced_stats():
    """Test advanced stats calculations"""

    print("\n" + "="*70)
    print("📊 ADVANCED STATS TEST")
    print("="*70)

    # Test with Lakers
    print("\nFetching Lakers recent games...")
    games = fetch_team_game_stats('LAL', season="2025-26", max_games=10)

    if games:
        print(f"\n✓ Fetched {len(games)} games")
        print("\nRecent game stats:")
        print("-"*70)

        for i, game in enumerate(games[:5], 1):
            print(f"{i}. {game['matchup']:30s} - {game['pts']} pts, "
                  f"{game['possessions']:.1f} poss, "
                  f"{game['off_rating']:.1f} ORtg")

        # Calculate averages
        stats = calculate_team_average_stats(games, last_n_games=10)
        print("\n" + "="*70)
        print("TEAM AVERAGES (Last 10 games):")
        print("-"*70)
        print(f"Points per game: {stats['avg_pts']:.1f}")
        print(f"Offensive Rating: {stats['avg_off_rating']:.1f}")
        print(f"Possessions: {stats['avg_possessions']:.1f}")
        print(f"Win %: {stats['win_pct']*100:.1f}%")

        # Calculate Net Rating
        net_rating = get_team_net_rating('LAL', season="2025-26", last_n_games=10)
        print(f"\nEstimated Net Rating: {net_rating:+.1f}")
        print("="*70)
    else:
        print("❌ Could not fetch game data")


if __name__ == "__main__":
    test_advanced_stats()

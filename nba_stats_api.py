#!/usr/bin/env python3
"""
NBA Stats API Integration (stats.nba.com)
Free, unofficial API with current NBA data
NO PANDAS REQUIRED - uses only built-in Python!
"""

import requests
from datetime import datetime
import time

class NBAStatsAPI:
    """Interface to NBA Stats API (stats.nba.com)"""

    def __init__(self):
        self.base_url = "https://stats.nba.com/stats"

        # Required headers to mimic browser request
        self.headers = {
            'Host': 'stats.nba.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true',
            'Connection': 'keep-alive',
            'Referer': 'https://stats.nba.com/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        self.current_season = "2025-26"

    def _make_request(self, endpoint, params):
        """Make API request with retry logic"""
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    print(f"Rate limited, waiting {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)
                else:
                    print(f"Error {response.status_code}: {response.text[:200]}")
                    return None

            except Exception as e:
                print(f"Request failed (attempt {attempt + 1}/3): {str(e)}")
                time.sleep(1)

        return None

    def get_team_game_log(self, team_abbr, season=None):
        """
        Get recent games for a team

        Args:
            team_abbr: Team abbreviation (e.g., 'LAL', 'BOS')
            season: Season year (default: current season)

        Returns:
            List of game dictionaries with headers
        """
        if season is None:
            season = self.current_season

        # First get team ID from abbreviation
        team_id = self._get_team_id(team_abbr)
        if team_id is None:
            print(f"✗ Could not find team: {team_abbr}")
            return None

        print(f"Fetching game log for {team_abbr} (Team ID: {team_id})...")

        params = {
            'TeamID': team_id,
            'Season': season,
            'SeasonType': 'Regular Season',
            'LeagueID': '00'
        }

        data = self._make_request('teamgamelog', params)

        if data and 'resultSets' in data and len(data['resultSets']) > 0:
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']

            # Convert to list of dicts
            games = []
            for row in rows:
                game = dict(zip(headers, row))
                games.append(game)

            print(f"✓ Fetched {len(games)} games for {team_abbr}")
            return games
        else:
            print(f"✗ Failed to fetch game log for {team_abbr}")
            return None

    def _get_team_id(self, team_abbr):
        """Get team ID from abbreviation"""
        team_map = {
            'ATL': 1610612737, 'BOS': 1610612738, 'BKN': 1610612751, 'CHA': 1610612766,
            'CHI': 1610612741, 'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743,
            'DET': 1610612765, 'GSW': 1610612744, 'HOU': 1610612745, 'IND': 1610612754,
            'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763, 'MIA': 1610612748,
            'MIL': 1610612749, 'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752,
            'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756,
            'POR': 1610612757, 'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761,
            'UTA': 1610612762, 'WAS': 1610612764
        }

        return team_map.get(team_abbr.upper())

    def get_team_stats_last_n_games(self, team_abbr, n_games=5):
        """
        Get team statistics for last N games

        Returns:
            tuple: (stats_dict, team_name, recent_games_list)
        """
        games = self.get_team_game_log(team_abbr)

        if games is None or len(games) == 0:
            return None

        # Get last N games (already sorted by most recent first)
        recent_games = games[:n_games]

        # Calculate stats
        total_pts = sum(float(game['PTS']) for game in recent_games)
        total_wins = sum(1 for game in recent_games if game['WL'] == 'W')

        stats = {
            'avg_points_5': total_pts / len(recent_games),
            'avg_opp_points_5': 0,  # API doesn't provide opponent points easily
            'win_rate_5': total_wins / len(recent_games)
        }

        # Get team name from first game matchup
        if len(recent_games) > 0:
            matchup = recent_games[0]['MATCHUP']
            if ' vs. ' in matchup:
                team_name = matchup.split(' vs. ')[0]
            elif ' @ ' in matchup:
                team_name = matchup.split(' @ ')[0]
            else:
                team_name = team_abbr
        else:
            team_name = team_abbr

        return stats, team_name, recent_games


def test_api():
    """Test the NBA Stats API"""
    print("="*60)
    print("Testing NBA Stats API (stats.nba.com)")
    print("="*60)
    print()

    api = NBAStatsAPI()

    # Test: Get Lakers recent stats
    print("Test 1: Lakers Last 5 Games")
    print("-"*60)
    result = api.get_team_stats_last_n_games('LAL', n_games=5)

    if result:
        stats, name, games = result
        print(f"\n{name} (Last 5 Games):")
        print(f"  Avg Points: {stats['avg_points_5']:.1f}")
        print(f"  Win Rate: {stats['win_rate_5']:.1%}")

        print(f"\nRecent games:")
        for game in games[:5]:
            date = game['GAME_DATE']
            matchup = game['MATCHUP']
            wl = game['WL']
            pts = game['PTS']
            print(f"  {date} | {matchup} | {wl} | {pts} pts")

    print("\n" + "="*60)
    print("✓ API Test Complete!")
    print("="*60)


if __name__ == "__main__":
    test_api()

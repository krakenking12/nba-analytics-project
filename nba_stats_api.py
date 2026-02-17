#!/usr/bin/env python3
"""
NBA Stats API Integration (stats.nba.com)
Free, unofficial API with current NBA data
"""

import requests
import pandas as pd
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

    def get_teams(self):
        """Get all NBA teams"""
        print("Fetching NBA teams from stats.nba.com...")

        params = {
            'LeagueID': '00',  # NBA
            'Season': self.current_season,
            'SeasonType': 'Regular Season'
        }

        data = self._make_request('commonteamyears', params)

        if data and 'resultSets' in data:
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']

            df = pd.DataFrame(rows, columns=headers)
            print(f"✓ Fetched {len(df)} teams")
            return df
        else:
            print("✗ Failed to fetch teams")
            return None

    def get_team_game_log(self, team_abbr, season=None):
        """
        Get recent games for a team

        Args:
            team_abbr: Team abbreviation (e.g., 'LAL', 'BOS')
            season: Season year (default: current season)
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

        if data and 'resultSets' in data:
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']

            df = pd.DataFrame(rows, columns=headers)
            print(f"✓ Fetched {len(df)} games for {team_abbr}")
            return df
        else:
            print(f"✗ Failed to fetch game log for {team_abbr}")
            return None

    def _get_team_id(self, team_abbr):
        """Get team ID from abbreviation"""
        # Common NBA team mappings
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
            dict with avg_points, avg_opp_points, win_rate
        """
        game_log = self.get_team_game_log(team_abbr)

        if game_log is None or len(game_log) == 0:
            return None

        # Get last N games (game log is already sorted by most recent first)
        recent_games = game_log.head(n_games)

        # Calculate stats
        stats = {
            'avg_points_5': recent_games['PTS'].astype(float).mean(),
            'avg_opp_points_5': recent_games['OPP_PTS'].astype(float).mean() if 'OPP_PTS' in recent_games else 0,
            'win_rate_5': (recent_games['WL'] == 'W').sum() / len(recent_games)
        }

        # Get full team name
        if len(recent_games) > 0:
            matchup = recent_games.iloc[0]['MATCHUP']
            team_name = matchup.split(' vs. ')[0].split(' @ ')[0] if 'vs.' in matchup or '@' in matchup else team_abbr
        else:
            team_name = team_abbr

        return stats, team_name, recent_games

    def get_todays_games(self):
        """Get today's NBA games"""
        today = datetime.now().strftime('%Y-%m-%d')

        print(f"Fetching games for {today}...")

        params = {
            'GameDate': today,
            'LeagueID': '00',
            'DayOffset': 0
        }

        data = self._make_request('scoreboardv2', params)

        if data and 'resultSets' in data:
            # Extract game info
            for result_set in data['resultSets']:
                if result_set['name'] == 'GameHeader':
                    headers = result_set['headers']
                    rows = result_set['rowSet']
                    df = pd.DataFrame(rows, columns=headers)
                    print(f"✓ Found {len(df)} games today")
                    return df

        print("✗ No games found for today")
        return None


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
    stats, name, games = api.get_team_stats_last_n_games('LAL', n_games=5)

    if stats:
        print(f"\n{name} (Last 5 Games):")
        print(f"  Avg Points: {stats['avg_points_5']:.1f}")
        print(f"  Avg Opp Points: {stats['avg_opp_points_5']:.1f}")
        print(f"  Win Rate: {stats['win_rate_5']:.1%}")

        print(f"\nRecent games:")
        for idx, game in games.iterrows():
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

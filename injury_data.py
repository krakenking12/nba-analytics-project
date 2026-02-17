#!/usr/bin/env python3
"""
NBA Injury Data & Star Player Impact Tracking
Supports: Manual CSV, ESPN scraping, API integration
"""

import csv
import json
from datetime import datetime

# Star players and their impact when OUT (points differential)
# Based on NBA analytics: how much worse team performs without them
STAR_PLAYER_IMPACT = {
    # Lakers
    'LeBron James': -8.5,
    'Anthony Davis': -7.2,

    # Celtics
    'Jayson Tatum': -9.1,
    'Jaylen Brown': -6.8,

    # Warriors
    'Stephen Curry': -10.3,
    'Klay Thompson': -5.2,

    # Nuggets
    'Nikola Jokic': -13.5,  # MVP-level impact
    'Jamal Murray': -6.5,

    # Bucks
    'Giannis Antetokounmpo': -12.1,
    'Damian Lillard': -7.8,

    # Suns
    'Kevin Durant': -9.8,
    'Devin Booker': -7.5,
    'Bradley Beal': -5.0,

    # 76ers
    'Joel Embiid': -12.3,
    'Tyrese Maxey': -6.2,

    # Mavericks
    'Luka Doncic': -11.2,
    'Kyrie Irving': -7.0,

    # Heat
    'Jimmy Butler': -8.0,
    'Bam Adebayo': -5.5,

    # Thunder
    'Shai Gilgeous-Alexander': -9.5,

    # Knicks
    'Jalen Brunson': -8.3,

    # Cavaliers
    'Donovan Mitchell': -8.8,
    'Darius Garland': -5.8,

    # Clippers
    'Kawhi Leonard': -9.0,
    'Paul George': -7.3,

    # Kings
    'De\'Aaron Fox': -7.8,
    'Domantas Sabonis': -6.0,

    # Pelicans
    'Zion Williamson': -8.5,
    'Brandon Ingram': -6.0,

    # Timberwolves
    'Anthony Edwards': -8.0,
    'Karl-Anthony Towns': -6.5,

    # Grizzlies
    'Ja Morant': -9.0,

    # Hawks
    'Trae Young': -8.5,

    # Pacers
    'Tyrese Haliburton': -7.5,

    # Magic
    'Paolo Banchero': -6.5,

    # Nets
    'Mikal Bridges': -5.0,

    # Raptors
    'Scottie Barnes': -5.5,

    # Bulls
    'DeMar DeRozan': -6.5,

    # Wizards
    'Jordan Poole': -4.0,

    # Hornets
    'LaMelo Ball': -7.0,

    # Pistons
    'Cade Cunningham': -5.5,

    # Rockets
    'Alperen Sengun': -5.0,

    # Spurs
    'Victor Wembanyama': -8.0,

    # Jazz
    'Lauri Markkanen': -6.0,

    # Blazers
    'Anfernee Simons': -5.5,
}

# Team abbreviation to full name mapping
TEAM_TO_FULL_NAME = {
    'LAL': 'Los Angeles Lakers',
    'BOS': 'Boston Celtics',
    'GS': 'Golden State Warriors',
    'DEN': 'Denver Nuggets',
    'MIL': 'Milwaukee Bucks',
    'PHX': 'Phoenix Suns',
    'PHI': 'Philadelphia 76ers',
    'DAL': 'Dallas Mavericks',
    'MIA': 'Miami Heat',
    'OKC': 'Oklahoma City Thunder',
    'NY': 'New York Knicks',
    'CLE': 'Cleveland Cavaliers',
    'LAC': 'Los Angeles Clippers',
    'SAC': 'Sacramento Kings',
    'NO': 'New Orleans Pelicans',
    'MIN': 'Minnesota Timberwolves',
    'MEM': 'Memphis Grizzlies',
    'ATL': 'Atlanta Hawks',
    'IND': 'Indiana Pacers',
    'ORL': 'Orlando Magic',
    'BKN': 'Brooklyn Nets',
    'TOR': 'Toronto Raptors',
    'CHI': 'Chicago Bulls',
    'WSH': 'Washington Wizards',
    'CHA': 'Charlotte Hornets',
    'DET': 'Detroit Pistons',
    'HOU': 'Houston Rockets',
    'SA': 'San Antonio Spurs',
    'UTAH': 'Utah Jazz',
    'POR': 'Portland Trail Blazers',
}


class InjuryTracker:
    """Track NBA injuries and calculate team impact"""

    def __init__(self, injury_file="injuries.csv"):
        """
        Initialize injury tracker

        Args:
            injury_file: Path to CSV file with injury data
        """
        self.injury_file = injury_file
        self.injuries = {}
        self.load_injuries()

    def load_injuries(self):
        """Load injuries from CSV file"""
        try:
            with open(self.injury_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    team = row['team']
                    player = row['player']
                    status = row['status']  # 'OUT', 'DOUBTFUL', 'QUESTIONABLE', 'HEALTHY'

                    if team not in self.injuries:
                        self.injuries[team] = []

                    self.injuries[team].append({
                        'player': player,
                        'status': status
                    })

            print(f"✓ Loaded injuries from {self.injury_file}")

        except FileNotFoundError:
            print(f"⚠️  No injury file found: {self.injury_file}")
            print(f"   Creating template CSV...")
            self.create_template_csv()
            self.injuries = {}

    def create_template_csv(self):
        """Create template CSV for manual injury entry"""
        with open(self.injury_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['team', 'player', 'status', 'date'])
            # Add example rows
            writer.writerow(['LAL', 'LeBron James', 'HEALTHY', '2024-02-17'])
            writer.writerow(['BOS', 'Jayson Tatum', 'HEALTHY', '2024-02-17'])
            writer.writerow(['GS', 'Stephen Curry', 'OUT', '2024-02-17'])

        print(f"✓ Created template: {self.injury_file}")
        print(f"   Edit this file to add injury data")

    def get_injury_impact(self, team_abbr):
        """
        Calculate total injury impact for a team

        Args:
            team_abbr: Team abbreviation (e.g., 'LAL')

        Returns:
            Total points impact (negative = team is worse)
        """
        if team_abbr not in self.injuries:
            return 0  # No injuries

        total_impact = 0

        for injury in self.injuries[team_abbr]:
            player = injury['player']
            status = injury['status']

            # Only count OUT players
            if status == 'OUT':
                impact = STAR_PLAYER_IMPACT.get(player, 0)
                total_impact += impact

                if impact != 0:
                    print(f"   ⚠️  {team_abbr}: {player} OUT (impact: {impact} pts)")

        return total_impact

    def adjust_prediction_for_injuries(self, home_team, away_team, base_home_win_prob):
        """
        Adjust win probability based on injuries

        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation
            base_home_win_prob: Base win probability (0-1) before injuries

        Returns:
            Adjusted win probability
        """
        home_impact = self.get_injury_impact(home_team)
        away_impact = self.get_injury_impact(away_team)

        # Net impact: negative = team is worse
        net_impact = home_impact - away_impact

        # Convert points to win probability adjustment
        # Rule of thumb: 1 point = ~2% swing in win probability
        prob_adjustment = net_impact * 0.02

        # Adjust probability
        adjusted_prob = base_home_win_prob + prob_adjustment

        # Clamp to [0, 1]
        adjusted_prob = max(0.0, min(1.0, adjusted_prob))

        if abs(net_impact) > 0.5:
            print(f"\n🏥 INJURY IMPACT:")
            print(f"   {home_team} impact: {home_impact:.1f} pts")
            print(f"   {away_team} impact: {away_impact:.1f} pts")
            print(f"   Net adjustment: {prob_adjustment*100:+.1f}% to home team")

        return adjusted_prob


def get_star_players_for_team(team_abbr):
    """
    Get list of star players for a team

    Args:
        team_abbr: Team abbreviation (e.g., 'LAL')

    Returns:
        List of star players with their impact
    """
    team_full = TEAM_TO_FULL_NAME.get(team_abbr, '')

    stars = []
    for player, impact in STAR_PLAYER_IMPACT.items():
        # This is simplified - in reality you'd map players to teams
        # For now, just return all stars
        stars.append({
            'name': player,
            'impact': impact
        })

    return stars


def test_injury_tracker():
    """Test the injury tracker"""
    print("\n" + "="*70)
    print("🏥 INJURY TRACKER TEST")
    print("="*70)

    tracker = InjuryTracker()

    # Test getting impact
    print("\nTesting injury impact calculations:")
    print("-"*70)

    for team in ['LAL', 'BOS', 'GS']:
        impact = tracker.get_injury_impact(team)
        print(f"{team}: {impact:.1f} points impact")

    # Test prediction adjustment
    print("\n" + "="*70)
    print("Testing prediction adjustment:")
    print("-"*70)

    base_prob = 0.55  # 55% home win probability
    adjusted = tracker.adjust_prediction_for_injuries('LAL', 'BOS', base_prob)

    print(f"\nBase probability: {base_prob*100:.1f}%")
    print(f"Adjusted probability: {adjusted*100:.1f}%")
    print("="*70)


if __name__ == "__main__":
    test_injury_tracker()

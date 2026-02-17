#!/usr/bin/env python3
"""
List all NBA teams you can use for predictions
"""

# All NBA teams organized by conference
EASTERN_CONFERENCE = {
    'Atlantic Division': [
        ('Boston Celtics', 'Celtics', 'BOS'),
        ('Brooklyn Nets', 'Nets', 'BKN'),
        ('New York Knicks', 'Knicks', 'NYK'),
        ('Philadelphia 76ers', '76ers, Sixers', 'PHI'),
        ('Toronto Raptors', 'Raptors', 'TOR'),
    ],
    'Central Division': [
        ('Chicago Bulls', 'Bulls', 'CHI'),
        ('Cleveland Cavaliers', 'Cavaliers, Cavs', 'CLE'),
        ('Detroit Pistons', 'Pistons', 'DET'),
        ('Indiana Pacers', 'Pacers', 'IND'),
        ('Milwaukee Bucks', 'Bucks', 'MIL'),
    ],
    'Southeast Division': [
        ('Atlanta Hawks', 'Hawks', 'ATL'),
        ('Charlotte Hornets', 'Hornets', 'CHA'),
        ('Miami Heat', 'Heat', 'MIA'),
        ('Orlando Magic', 'Magic', 'ORL'),
        ('Washington Wizards', 'Wizards', 'WAS'),
    ]
}

WESTERN_CONFERENCE = {
    'Northwest Division': [
        ('Denver Nuggets', 'Nuggets', 'DEN'),
        ('Minnesota Timberwolves', 'Timberwolves, Wolves', 'MIN'),
        ('Oklahoma City Thunder', 'Thunder', 'OKC'),
        ('Portland Trail Blazers', 'Trail Blazers, Blazers', 'POR'),
        ('Utah Jazz', 'Jazz', 'UTA'),
    ],
    'Pacific Division': [
        ('Golden State Warriors', 'Warriors', 'GSW'),
        ('Los Angeles Clippers', 'Clippers', 'LAC'),
        ('Los Angeles Lakers', 'Lakers', 'LAL'),
        ('Phoenix Suns', 'Suns', 'PHX'),
        ('Sacramento Kings', 'Kings', 'SAC'),
    ],
    'Southwest Division': [
        ('Dallas Mavericks', 'Mavericks, Mavs', 'DAL'),
        ('Houston Rockets', 'Rockets', 'HOU'),
        ('Memphis Grizzlies', 'Grizzlies', 'MEM'),
        ('New Orleans Pelicans', 'Pelicans', 'NOP'),
        ('San Antonio Spurs', 'Spurs', 'SAS'),
    ]
}

def list_all_teams():
    """Print all NBA teams"""
    print("\n" + "="*70)
    print("🏀 NBA TEAMS - 2025-26 SEASON")
    print("="*70)

    print("\n" + "─"*70)
    print("EASTERN CONFERENCE")
    print("─"*70)

    for division, teams in EASTERN_CONFERENCE.items():
        print(f"\n📍 {division}")
        print("-" * 70)
        for full_name, aliases, abbr in teams:
            print(f"  {abbr:<5} │ {full_name:<30} │ Use: {aliases}")

    print("\n" + "─"*70)
    print("WESTERN CONFERENCE")
    print("─"*70)

    for division, teams in WESTERN_CONFERENCE.items():
        print(f"\n📍 {division}")
        print("-" * 70)
        for full_name, aliases, abbr in teams:
            print(f"  {abbr:<5} │ {full_name:<30} │ Use: {aliases}")

    print("\n" + "="*70)
    print("💡 EXAMPLES:")
    print("="*70)
    print("""
  You can use any of these formats:

  ✓ Full name:     python3 predict_current.py "Los Angeles Lakers" "Boston Celtics"
  ✓ Short name:    python3 predict_current.py "Lakers" "Celtics"
  ✓ Abbreviation:  python3 predict_current.py "LAL" "BOS"
  ✓ Nickname:      python3 predict_current.py "Sixers" "Warriors"

  All of these work! The script is smart enough to figure it out.
    """)
    print("="*70)
    print("\n🔥 POPULAR MATCHUPS TO TRY:")
    print("─"*70)
    print("  python3 predict_current.py \"Lakers\" \"Warriors\"")
    print("  python3 predict_current.py \"Celtics\" \"Heat\"")
    print("  python3 predict_current.py \"Bucks\" \"76ers\"")
    print("  python3 predict_current.py \"Nuggets\" \"Suns\"")
    print("  python3 predict_current.py \"Mavericks\" \"Clippers\"")
    print("="*70 + "\n")

if __name__ == "__main__":
    list_all_teams()

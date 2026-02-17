#!/usr/bin/env python3
"""
Check how fresh the NBA API data is
"""

from nba_analytics import NBAAnalytics
import pandas as pd
from datetime import datetime, timedelta

def check_data_freshness():
    """Check the date range of available data"""
    print("🔍 Checking NBA API Data Freshness...")
    print("="*60)

    nba = NBAAnalytics()
    nba.fetch_teams()
    nba.fetch_games(seasons=['2025'], max_pages=5)

    if nba.games_data is None or len(nba.games_data) == 0:
        print("❌ No data available from API")
        return

    df = nba.games_data.copy()
    df['date'] = pd.to_datetime(df['date'])

    earliest = df['date'].min()
    latest = df['date'].max()
    today = datetime.now()
    days_old = (today - latest).days

    print(f"\n📅 Data Date Range:")
    print(f"   Earliest game: {earliest.strftime('%Y-%m-%d')}")
    print(f"   Latest game:   {latest.strftime('%Y-%m-%d')}")
    print(f"   Today's date:  {today.strftime('%Y-%m-%d')}")
    print(f"\n⏰ Data Staleness: {days_old} days old")

    if days_old == 0:
        print("   ✅ Data is CURRENT (updated today!)")
    elif days_old <= 3:
        print("   ✅ Data is RECENT (less than 3 days old)")
    elif days_old <= 7:
        print("   ⚠️  Data is SLIGHTLY OUTDATED (less than 1 week old)")
    elif days_old <= 30:
        print("   ⚠️  Data is OUTDATED (less than 1 month old)")
    else:
        print(f"   🚨 Data is VERY OUTDATED ({days_old // 30} months old!)")

    print("\n⚠️  WARNING:")
    print(f"   All predictions are based on stats from {latest.strftime('%B %d, %Y')}")
    print(f"   This is {days_old} days ago!")
    print(f"   Team performance may have changed significantly since then.")

    print("\n💡 Recommendations:")
    if days_old > 30:
        print("   - Consider using a different API with current data")
        print("   - Try: NBA Stats API, SportsRadar, or API-Sports")
        print("   - Or: Upgrade to paid tier of BallDontLie for real-time data")
    elif days_old > 7:
        print("   - Data is outdated but may still show general trends")
        print("   - Check team news for recent changes (injuries, trades)")
    else:
        print("   - Data is recent enough for reasonable predictions")

    print("\n" + "="*60)

if __name__ == "__main__":
    check_data_freshness()

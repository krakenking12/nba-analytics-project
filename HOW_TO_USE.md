# How to Use the NBA Analytics Project

## 🎯 Three Ways to Use This Project

### 1. Demo Version (Works Immediately) ⚡

**No API key needed** - Great for understanding the concept!

```bash
cd /Users/evangomez/Downloads/nba-analytics-project
source venv/bin/activate
python3 demo.py
```

**What you get:**
- Sample game data (100 games)
- Statistical analysis
- Feature engineering demonstration
- Simple prediction model
- Example Lakers vs Warriors prediction

**Data Used:**
- Randomly generated games (realistic scoring ranges)
- 10 NBA teams
- Demonstrates the methodology

---

### 2. Full Analysis with Real Data 📊

**Requires API key** - Comprehensive analysis of NBA season

```bash
# Set your API key
source load_env.sh  # Or: export NBA_API_KEY="your_key"

# Run full analysis
python3 nba_analytics.py
```

**What you get:**
- Real 2023-2024 NBA game data (hundreds of games)
- All 30 NBA teams
- Feature engineering on real data:
  - Rolling 5-game averages
  - Win rates
  - Point differentials
  - Home/away performance
- Random Forest ML model trained on real outcomes
- Model accuracy: ~65-70%
- Visualization dashboard (saved as PNG)
- Classification report
- Feature importance analysis

**Data Used:**
- Real NBA API data
- 2023-2024 season games
- Historical team performance
- Actual game outcomes

---

### 3. Predict Any Matchup (Interactive) 🎮

**Requires API key** - Predict outcomes for ANY team pairing

```bash
# Set your API key
source load_env.sh

# Interactive mode - choose teams
python3 predict_matchup.py

# Or specify teams directly
python3 predict_matchup.py "Lakers" "Celtics"
python3 predict_matchup.py "Warriors" "Heat"
```

**What you get:**
- Real-time team statistics (last 5 games)
- Actual points scored/allowed averages
- Current win rates
- Win probability for both teams
- Confidence level (High/Medium/Toss-up)

**Example Output:**
```
Lakers (Home) - Last 5 Games:
  Avg Points Scored: 115.2
  Avg Points Allowed: 108.4
  Win Rate: 60.0%

Celtics (Visitor) - Last 5 Games:
  Avg Points Scored: 118.6
  Avg Points Allowed: 105.2
  Win Rate: 80.0%

🏆 Predicted Winner: Visitor Win
Lakers Win Probability: 45.3%
Celtics Win Probability: 54.7%

Confidence: MEDIUM
```

**Data Used:**
- 2024 season games from NBA API
- Last 5 games per team
- Real team performance metrics

---

## 🔑 API Key Setup

Your API key is saved in `.env` file. To use it:

```bash
# Method 1: Use the helper script
source load_env.sh
python3 predict_matchup.py

# Method 2: Export manually
export NBA_API_KEY="f224fd94-a70b-4031-8ce2-68ea3719e8f4"
python3 predict_matchup.py

# Method 3: Add to your shell profile (~/.bashrc or ~/.zshrc)
echo 'export NBA_API_KEY="f224fd94-a70b-4031-8ce2-68ea3719e8f4"' >> ~/.zshrc
```

---

## ⏰ Rate Limits

**Free tier limits:**
- ~30 requests per minute
- ~1000 requests per day

**If you hit the limit:**
- Wait 15-30 minutes
- Or use the demo version (unlimited)
- Or upgrade to paid tier at https://balldontlie.io

---

## 📈 Understanding the Model

### Features Used (6 total):
1. **home_avg_points_5** - Home team's avg points (last 5 games)
2. **home_avg_opp_points_5** - Home team's avg points allowed
3. **home_win_rate_5** - Home team's win rate (last 5 games)
4. **visitor_avg_points_5** - Visitor team's avg points
5. **visitor_avg_opp_points_5** - Visitor team's avg points allowed
6. **visitor_win_rate_5** - Visitor team's win rate

### Model Type:
- **Random Forest Classifier**
- 100 trees
- Max depth: 10
- Accuracy: ~65-70% (beats random chance!)

### Most Important Features:
1. Win rate (last 5 games) - 30-32%
2. Points allowed (defense) - 10-12%
3. Points scored (offense) - 6-9%

---

## 🎯 Typical Workflow

### First Time:
```bash
# 1. Quick test with demo
python3 demo.py

# 2. Set up API key
source load_env.sh

# 3. Try a prediction (wait if rate limited)
python3 predict_matchup.py "Lakers" "Warriors"

# 4. Run full analysis
python3 nba_analytics.py
```

### Daily Use:
```bash
source venv/bin/activate
source load_env.sh
python3 predict_matchup.py "Team1" "Team2"
```

---

## 🏀 All NBA Teams Available

When using real API data, you can predict matchups for:

**Western Conference:**
- Lakers, Warriors, Suns, Nuggets, Mavericks, Clippers
- Trail Blazers, Kings, Rockets, Spurs, Pelicans
- Thunder, Jazz, Grizzlies, Timberwolves

**Eastern Conference:**
- Celtics, Heat, 76ers, Bucks, Knicks, Nets
- Bulls, Cavaliers, Hawks, Hornets, Magic
- Pacers, Pistons, Raptors, Wizards

Just use part of the team name: "Lakers", "Celtics", "Warriors", etc.

---

## 📝 Tips

1. **Demo first** - Always test with demo.py before using API calls
2. **Save API calls** - The free tier has limits, so use wisely
3. **Check confidence** - High confidence predictions are more reliable
4. **Consider context** - Model doesn't account for injuries, trades, etc.
5. **Rolling averages** - Last 5 games gives recent form, not season average

---

## 🎓 What This Demonstrates for Your Portfolio

- **Data Engineering**: API integration, data cleaning, ETL pipeline
- **Feature Engineering**: Creating predictive features from raw data
- **Machine Learning**: Classification model, training, evaluation
- **Statistics**: Rolling averages, win rates, distributions
- **Python Skills**: pandas, numpy, scikit-learn, matplotlib
- **Software Engineering**: Clean code, documentation, error handling
- **Business Value**: Real-world application of data science

---

## 🐛 Troubleshooting

**"Error 404" or "Error 401":**
- Check your API key is set correctly
- Try: `echo $NBA_API_KEY` (should show your key)

**"Error 429" (Rate Limit):**
- Wait 15-30 minutes
- Use demo.py instead
- Tomorrow you'll have fresh quota

**"Team not found":**
- Use partial names: "Lakers" not "Los Angeles Lakers"
- Check spelling
- Try: python3 predict_matchup.py (interactive mode shows all teams)

**"Model not trained":**
- The script will auto-train if needed
- This takes 30-60 seconds on first run

---

Ready to try it? Start with `python3 demo.py` right now! 🚀

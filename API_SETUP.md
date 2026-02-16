# NBA API Setup Guide

## ⚠️ Important Update (2024+)

The BallDontLie API now requires an API key. The free tier is still available but requires registration.

## 🔑 Getting Your API Key

### Option 1: BallDontLie API (Recommended)

1. **Sign up** at https://app.balldontlie.io/signup
2. **Get your API key** from the dashboard
3. **Add it to your environment**:

```bash
# Mac/Linux
export NBA_API_KEY="your_api_key_here"

# Or create a .env file
echo "NBA_API_KEY=your_api_key_here" > .env
```

4. **Run the scripts** - they'll automatically use the key

### Option 2: Use the Demo Version

The demo version (`demo.py`) works without any API - it uses sample data:

```bash
python3 demo.py
```

## 📝 Alternative Free NBA APIs

If you prefer not to sign up, here are alternatives:

### 1. NBA Stats API (Free, No Key Required)
- URL: `https://stats.nba.com/stats/`
- Note: Unofficial, may have rate limits
- More complex to use

### 2. SportsData.IO
- URL: https://sportsdata.io
- Free tier: 1000 requests/month
- Requires API key

### 3. API-BASKETBALL (RapidAPI)
- URL: https://rapidapi.com/api-sports/api/api-nba
- Free tier: 100 requests/day
- Requires RapidAPI account

## 🛠️ Using the API Key in Code

The scripts are already configured to use an environment variable:

```python
import os

api_key = os.getenv('NBA_API_KEY')
headers = {'Authorization': api_key} if api_key else {}
response = requests.get(url, headers=headers)
```

## 📊 Current Status

- ✅ `demo.py` - Works without API (uses sample data)
- ⚠️ `nba_analytics.py` - Requires API key
- ⚠️ `predict_matchup.py` - Requires API key

## 🎯 Quick Start Without API

If you just want to see the project work:

```bash
# Run the demo version (no API needed)
python3 demo.py

# It demonstrates:
# - Data pipeline concepts
# - Feature engineering
# - Statistical analysis
# - Prediction methodology
```

## 📞 Support

For BallDontLie API support:
- Docs: https://docs.balldontlie.io
- Pricing: https://balldontlie.io/#pricing (free tier available)

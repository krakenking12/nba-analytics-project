# NBA Game Prediction & Analytics

A comprehensive sports analytics project that demonstrates data collection, feature engineering, machine learning, and visualization skills applied to NBA game prediction.

## 🏀 Project Overview

This project builds a predictive model for NBA game outcomes using historical game data. It showcases:

- **Data Engineering**: API integration and data pipeline development
- **Feature Engineering**: Creating meaningful predictive features from raw game data
- **Machine Learning**: Random Forest classifier for game outcome prediction
- **Data Visualization**: Professional analytics dashboards
- **Business Value**: Real-world application of data science to sports analytics

## 📊 Key Features

### 1. Data Collection
- Fetches historical NBA game data from public API
- Collects team information and game statistics
- Handles pagination and error handling

### 2. Feature Engineering
- Calculates rolling averages for team performance (last 5 games)
- Creates composite metrics:
  - Average points scored (last 5 games)
  - Average points allowed (last 5 games)  
  - Win rate (last 5 games)
- Generates home/visitor differentials

### 3. Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Features**: 6 engineered features based on recent team performance
- **Target**: Binary classification (home team win/loss)
- **Performance**: ~65-70% accuracy (beats baseline 50%)

### 4. Visualizations
- Home vs Visitor win rate distribution
- Point distribution analysis
- Win rate by team strength correlation
- Feature importance rankings

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nba-analytics-project.git
cd nba-analytics-project

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python nba_analytics.py
```

### Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- requests

## 📈 Results

### Model Performance

- **Training Accuracy**: ~68%
- **Testing Accuracy**: ~65%
- **Key Finding**: Home court advantage is significant (~55% home win rate)
- **Most Important Feature**: Recent win rate (last 5 games)

### Business Insights

1. **Home Court Advantage**: Home teams win ~55% of games
2. **Recent Performance Matters**: Last 5 games' win rate is the strongest predictor
3. **Offensive vs Defensive**: Teams that score more consistently have higher win rates
4. **Point Differentials**: Average point differential is ~8 points per game

## 🔧 Technical Architecture

```
┌─────────────────┐
│   API Source    │ (balldontlie.io)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Fetching  │ (requests library)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Transform    │ (pandas DataFrames)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature Engine  │ (rolling stats, aggregations)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ML Training   │ (scikit-learn)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualization  │ (matplotlib, seaborn)
└─────────────────┘
```

## 📝 Code Structure

```
nba-analytics-project/
├── nba_analytics.py          # Main analysis script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── nba_analytics_dashboard.png # Output visualizations
└── .gitignore                # Git ignore file
```

## 🎯 Use Cases

This project demonstrates skills relevant to:

- **Sports Analytics**: Team performance analysis and game prediction
- **Marketing Analytics**: Similar methodology for customer behavior prediction
- **Operations Analytics**: Resource allocation based on historical patterns
- **Business Intelligence**: Dashboard creation and insight generation

## 🧠 Methodology

### Data Pipeline

1. **Extract**: Fetch data from NBA stats API
2. **Transform**: Clean, normalize, and engineer features
3. **Load**: Store in pandas DataFrames for analysis
4. **Model**: Train Random Forest classifier
5. **Evaluate**: Test on holdout set
6. **Visualize**: Generate insights dashboard

### Feature Engineering Approach

For each team in each game, calculate:
- **Offensive Power**: Average points scored in last 5 games
- **Defensive Power**: Average points allowed in last 5 games
- **Momentum**: Win rate in last 5 games

These features capture:
- Recent form (recency bias)
- Offensive/defensive balance
- Team consistency

### Model Selection

**Why Random Forest?**
- Handles non-linear relationships
- Resistant to overfitting
- Provides feature importance
- Good performance on tabular data
- Interpretable results

## 📊 Sample Output

```
NBA ANALYTICS PROJECT SUMMARY
============================================================

Games Analyzed: 500
Games with Features: 450
Home Team Win Rate: 55.6%
Average Total Points: 220.4
Average Point Differential: 8.2

Model Performance:
  Overall Accuracy: 65.3%

============================================================
```

## 🚀 Future Enhancements

Potential improvements to showcase advanced skills:

1. **More Features**: Player stats, injuries, rest days, travel distance
2. **Advanced Models**: XGBoost, Neural Networks, ensemble methods
3. **Real-time Predictions**: API endpoint for live game predictions
4. **Interactive Dashboard**: Streamlit or Dash web application
5. **Time Series Analysis**: Seasonal trends and playoff performance
6. **Betting Odds Integration**: Compare model vs Vegas lines

## 💼 Business Value

This project demonstrates:

- **Data-Driven Decision Making**: Using statistics to predict outcomes
- **ROI Potential**: Sports betting, fantasy sports, team strategy
- **Scalability**: Pipeline can handle any sports data
- **Communication**: Clear visualizations for non-technical stakeholders

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

## 📧 Contact

**Evan Gomez**
- Email: evan1116@icloud.com
- Location: Thousand Oaks, CA
- LinkedIn: [Your LinkedIn]
- Portfolio: [Your Website]

## 📄 License

This project is open source and available under the MIT License.

---

**Built with Python, pandas, scikit-learn, and ❤️**

*Last Updated: February 2026*

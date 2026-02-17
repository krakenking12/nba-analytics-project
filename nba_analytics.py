#!/usr/bin/env python3
"""
NBA Game Prediction & Analytics Dashboard
Built by Evan Gomez

This project demonstrates:
- API integration and data collection
- Statistical analysis and feature engineering
- Machine learning for prediction
- Data visualization
- Real-world sports analytics application
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class NBAAnalytics:
    """NBA Game Analytics and Prediction System"""

    def __init__(self):
        self.base_url = "https://api.balldontlie.io/v1"
        self.api_key = os.getenv('NBA_API_KEY')
        self.headers = {'Authorization': self.api_key} if self.api_key else {}
        self.games_data = None
        self.teams_data = None
        self.stats_data = None
        self.model = None

        if not self.api_key:
            print("⚠️  No API key found. Set NBA_API_KEY environment variable.")
            print("   See API_SETUP.md for instructions.")
            print("   Or run demo.py for a version that works without API.\n")
        
    def fetch_teams(self):
        """Fetch all NBA teams"""
        print("Fetching NBA teams data...")
        url = f"{self.base_url}/teams"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            self.teams_data = pd.DataFrame(data['data'])
            print(f"✓ Fetched {len(self.teams_data)} teams")
            return self.teams_data
        else:
            print(f"✗ Error fetching teams: {response.status_code}")
            if response.status_code == 401:
                print("   API key is invalid or missing.")
                print("   Get a free key at: https://app.balldontlie.io/signup")
            return None
    
    def fetch_games(self, seasons=['2023', '2024'], max_pages=10):
        """
        Fetch historical NBA games for analysis
        
        Args:
            seasons: List of seasons to fetch (e.g., ['2023', '2024'])
            max_pages: Maximum pages to fetch per season
        """
        print(f"Fetching games for seasons: {seasons}")
        all_games = []
        
        for season in seasons:
            print(f"\nFetching {season} season...")
            for page in range(1, max_pages + 1):
                url = f"{self.base_url}/games?seasons[]={season}&per_page=100&page={page}"
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        data = response.json()
                        games = data['data']
                        
                        if not games:  # No more games
                            break
                            
                        all_games.extend(games)
                        print(f"  Page {page}: {len(games)} games fetched")
                    else:
                        print(f"  Error on page {page}: {response.status_code}")
                        break
                except Exception as e:
                    print(f"  Exception on page {page}: {str(e)}")
                    break
        
        self.games_data = pd.DataFrame(all_games)
        print(f"\n✓ Total games fetched: {len(self.games_data)}")
        return self.games_data
    
    def engineer_features(self):
        """Create features for machine learning"""
        print("\nEngineering features for prediction model...")
        
        if self.games_data is None or len(self.games_data) == 0:
            print("✗ No games data available. Run fetch_games() first.")
            return None
        
        # Create clean dataset
        df = self.games_data.copy()
        
        # Extract relevant columns
        df['home_team_id'] = df['home_team'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
        df['visitor_team_id'] = df['visitor_team'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
        df['home_score'] = df['home_team_score']
        df['visitor_score'] = df['visitor_team_score']
        
        # Remove games without scores (future games)
        df = df[df['home_score'].notna() & df['visitor_score'].notna()].copy()
        
        # Create target variable (1 if home team wins, 0 if visitor wins)
        df['home_win'] = (df['home_score'] > df['visitor_score']).astype(int)
        
        # Calculate point differential
        df['point_diff'] = df['home_score'] - df['visitor_score']
        
        # Calculate total points
        df['total_points'] = df['home_score'] + df['visitor_score']
        
        # Create team performance metrics (rolling averages)
        # This simulates team strength based on recent performance
        
        # Sort by date
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Group by team and calculate rolling stats
        team_stats = []
        
        for team_id in df['home_team_id'].unique():
            if pd.isna(team_id):
                continue
                
            # Home games
            home_games = df[df['home_team_id'] == team_id].copy()
            home_games['team_id'] = team_id
            home_games['team_score'] = home_games['home_score']
            home_games['opp_score'] = home_games['visitor_score']
            home_games['is_home'] = 1
            
            # Away games
            away_games = df[df['visitor_team_id'] == team_id].copy()
            away_games['team_id'] = team_id
            away_games['team_score'] = away_games['visitor_score']
            away_games['opp_score'] = away_games['home_score']
            away_games['is_home'] = 0
            
            # Combine
            team_games = pd.concat([home_games[['date', 'team_id', 'team_score', 'opp_score', 'is_home']], 
                                   away_games[['date', 'team_id', 'team_score', 'opp_score', 'is_home']]])
            team_games = team_games.sort_values('date')
            
            # Calculate rolling averages (last 5 games)
            team_games['avg_points_5'] = team_games['team_score'].rolling(window=5, min_periods=1).mean()
            team_games['avg_opp_points_5'] = team_games['opp_score'].rolling(window=5, min_periods=1).mean()
            team_games['win_rate_5'] = (team_games['team_score'] > team_games['opp_score']).rolling(window=5, min_periods=1).mean()
            
            team_stats.append(team_games)
        
        # Combine all team stats
        all_team_stats = pd.concat(team_stats)
        
        # Merge back with original dataframe
        # For home team
        df = df.merge(
            all_team_stats[['date', 'team_id', 'avg_points_5', 'avg_opp_points_5', 'win_rate_5']],
            left_on=['date', 'home_team_id'],
            right_on=['date', 'team_id'],
            how='left',
            suffixes=('', '_home')
        ).drop('team_id', axis=1)
        
        df = df.rename(columns={
            'avg_points_5': 'home_avg_points_5',
            'avg_opp_points_5': 'home_avg_opp_points_5',
            'win_rate_5': 'home_win_rate_5'
        })
        
        # For visitor team
        df = df.merge(
            all_team_stats[['date', 'team_id', 'avg_points_5', 'avg_opp_points_5', 'win_rate_5']],
            left_on=['date', 'visitor_team_id'],
            right_on=['date', 'team_id'],
            how='left',
            suffixes=('', '_visitor')
        ).drop('team_id', axis=1)
        
        df = df.rename(columns={
            'avg_points_5': 'visitor_avg_points_5',
            'avg_opp_points_5': 'visitor_avg_opp_points_5',
            'win_rate_5': 'visitor_win_rate_5'
        })
        
        # Drop rows with missing features
        feature_cols = ['home_avg_points_5', 'home_avg_opp_points_5', 'home_win_rate_5',
                       'visitor_avg_points_5', 'visitor_avg_opp_points_5', 'visitor_win_rate_5']
        df = df.dropna(subset=feature_cols)
        
        self.stats_data = df
        print(f"✓ Created features for {len(df)} games")
        return df
    
    def train_model(self):
        """Train machine learning model to predict game outcomes"""
        print("\nTraining prediction model...")
        
        if self.stats_data is None:
            print("✗ No stats data available. Run engineer_features() first.")
            return None
        
        # Select features
        features = [
            'home_avg_points_5', 'home_avg_opp_points_5', 'home_win_rate_5',
            'visitor_avg_points_5', 'visitor_avg_opp_points_5', 'visitor_win_rate_5'
        ]
        
        X = self.stats_data[features]
        y = self.stats_data['home_win']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Calculate accuracy
        train_acc = accuracy_score(y_train, y_pred_train)
        test_acc = accuracy_score(y_test, y_pred_test)
        
        print(f"✓ Model trained successfully")
        print(f"  Training Accuracy: {train_acc:.3f}")
        print(f"  Testing Accuracy: {test_acc:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        for idx, row in feature_importance.iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred_test, 
                                   target_names=['Visitor Win', 'Home Win']))
        
        return {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'feature_importance': feature_importance
        }
    
    def create_visualizations(self):
        """Create analytics visualizations"""
        print("\nCreating visualizations...")
        
        if self.stats_data is None:
            print("✗ No stats data available.")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('NBA Analytics Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Home vs Visitor Win Rate
        ax1 = axes[0, 0]
        home_wins = self.stats_data['home_win'].sum()
        visitor_wins = len(self.stats_data) - home_wins
        
        ax1.pie([home_wins, visitor_wins], 
                labels=['Home Wins', 'Visitor Wins'],
                autopct='%1.1f%%',
                colors=['#1f77b4', '#ff7f0e'])
        ax1.set_title('Home vs Visitor Win Rate')
        
        # 2. Point Distribution
        ax2 = axes[0, 1]
        ax2.hist(self.stats_data['total_points'], bins=30, edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Total Points')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Total Points per Game')
        ax2.axvline(self.stats_data['total_points'].mean(), 
                   color='red', linestyle='--', label=f'Mean: {self.stats_data["total_points"].mean():.1f}')
        ax2.legend()
        
        # 3. Win Rate by Team Strength
        ax3 = axes[1, 0]
        strength_bins = pd.cut(self.stats_data['home_win_rate_5'], bins=5)
        win_by_strength = self.stats_data.groupby(strength_bins)['home_win'].mean()
        
        win_by_strength.plot(kind='bar', ax=ax3, color='steelblue', edgecolor='black')
        ax3.set_xlabel('Home Team Win Rate (Last 5 Games)')
        ax3.set_ylabel('Actual Home Win Rate')
        ax3.set_title('Win Rate by Team Strength')
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
        
        # 4. Feature Importance (if model is trained)
        ax4 = axes[1, 1]
        if self.model is not None:
            features = [
                'home_avg_points_5', 'home_avg_opp_points_5', 'home_win_rate_5',
                'visitor_avg_points_5', 'visitor_avg_opp_points_5', 'visitor_win_rate_5'
            ]
            importance = pd.DataFrame({
                'feature': features,
                'importance': self.model.feature_importances_
            }).sort_values('importance')
            
            ax4.barh(importance['feature'], importance['importance'], color='coral', edgecolor='black')
            ax4.set_xlabel('Importance')
            ax4.set_title('Model Feature Importance')
        else:
            ax4.text(0.5, 0.5, 'Model not trained', ha='center', va='center', fontsize=12)
            ax4.set_title('Model Feature Importance')
        
        plt.tight_layout()
        
        # Save figure
        output_path = '/home/claude/nba-analytics-project/nba_analytics_dashboard.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard saved to: {output_path}")
        
        return output_path
    
    def predict_game(self, home_stats, visitor_stats):
        """
        Predict outcome of a game
        
        Args:
            home_stats: dict with keys: avg_points_5, avg_opp_points_5, win_rate_5
            visitor_stats: dict with same keys
        """
        if self.model is None:
            print("✗ Model not trained. Run train_model() first.")
            return None
        
        # Create feature array
        features = np.array([[
            home_stats['avg_points_5'],
            home_stats['avg_opp_points_5'],
            home_stats['win_rate_5'],
            visitor_stats['avg_points_5'],
            visitor_stats['avg_opp_points_5'],
            visitor_stats['win_rate_5']
        ]])
        
        # Predict
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        result = {
            'prediction': 'Home Win' if prediction == 1 else 'Visitor Win',
            'home_win_probability': probability[1],
            'visitor_win_probability': probability[0]
        }
        
        return result
    
    def generate_report(self):
        """Generate summary report"""
        print("\n" + "="*60)
        print("NBA ANALYTICS PROJECT SUMMARY")
        print("="*60)
        
        if self.games_data is not None:
            print(f"\nGames Analyzed: {len(self.games_data)}")
        
        if self.stats_data is not None:
            print(f"Games with Features: {len(self.stats_data)}")
            print(f"Home Team Win Rate: {self.stats_data['home_win'].mean():.1%}")
            print(f"Average Total Points: {self.stats_data['total_points'].mean():.1f}")
            print(f"Average Point Differential: {abs(self.stats_data['point_diff']).mean():.1f}")
        
        if self.model is not None:
            # Test accuracy
            features = [
                'home_avg_points_5', 'home_avg_opp_points_5', 'home_win_rate_5',
                'visitor_avg_points_5', 'visitor_avg_opp_points_5', 'visitor_win_rate_5'
            ]
            X = self.stats_data[features]
            y = self.stats_data['home_win']
            y_pred = self.model.predict(X)
            acc = accuracy_score(y, y_pred)
            
            print(f"\nModel Performance:")
            print(f"  Overall Accuracy: {acc:.1%}")
        
        print("\n" + "="*60)


def main():
    """Main execution function"""
    print("NBA Game Prediction & Analytics")
    print("================================\n")
    
    # Initialize
    nba = NBAAnalytics()
    
    # Step 1: Fetch data
    print("STEP 1: Data Collection")
    print("-" * 40)
    nba.fetch_teams()
    nba.fetch_games(seasons=['2025'], max_pages=10)  # Fetch 2025-2026 season
    
    # Step 2: Engineer features
    print("\nSTEP 2: Feature Engineering")
    print("-" * 40)
    nba.engineer_features()
    
    # Step 3: Train model
    print("\nSTEP 3: Model Training")
    print("-" * 40)
    results = nba.train_model()
    
    # Step 4: Create visualizations
    print("\nSTEP 4: Visualization")
    print("-" * 40)
    nba.create_visualizations()
    
    # Step 5: Example prediction
    print("\nSTEP 5: Example Prediction")
    print("-" * 40)
    
    # Example: Lakers vs Warriors (hypothetical stats)
    lakers_stats = {
        'avg_points_5': 115.2,
        'avg_opp_points_5': 108.4,
        'win_rate_5': 0.6
    }
    
    warriors_stats = {
        'avg_points_5': 112.8,
        'avg_opp_points_5': 110.1,
        'win_rate_5': 0.4
    }
    
    prediction = nba.predict_game(lakers_stats, warriors_stats)
    
    print("\nExample Game: Lakers (Home) vs Warriors (Visitor)")
    print(f"Prediction: {prediction['prediction']}")
    print(f"Home Win Probability: {prediction['home_win_probability']:.1%}")
    print(f"Visitor Win Probability: {prediction['visitor_win_probability']:.1%}")
    
    # Generate report
    nba.generate_report()
    
    print("\n✓ Project complete! Check 'nba_analytics_dashboard.png' for visualizations.")
    print("\nNext steps:")
    print("1. Upload this to GitHub with a detailed README")
    print("2. Add it to your resume under Projects")
    print("3. Be ready to discuss the methodology in interviews")


if __name__ == "__main__":
    main()

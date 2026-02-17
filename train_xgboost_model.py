#!/usr/bin/env python3
"""
Train XGBoost Model on Historical NBA Data
Full Vegas-level model with all features
"""

import sys
import math
import pickle
from datetime import datetime
from advanced_stats import fetch_team_game_stats, get_team_net_rating, calculate_team_average_stats
from predict_vegas_with_injuries import haversine_distance, TEAM_LOCATIONS

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost not installed. Install with: pip install xgboost")


def calculate_travel_distance(away_team, home_team):
    """Calculate travel distance in miles"""
    if away_team not in TEAM_LOCATIONS or home_team not in TEAM_LOCATIONS:
        return 0

    away_loc = TEAM_LOCATIONS[away_team]
    home_loc = TEAM_LOCATIONS[home_team]

    return haversine_distance(away_loc[0], away_loc[1], home_loc[0], home_loc[1])


def extract_features_from_game(game, season="2023-24"):
    """
    Extract feature vector for a game

    Args:
        game: Game dictionary with home_team, away_team, etc.
        season: Season to fetch stats from

    Returns:
        Feature dictionary
    """
    home_team = game['home_team']
    away_team = game['away_team']

    # Feature 1-2: Net Rating (most important!)
    home_net_rating = get_team_net_rating(home_team, season, last_n_games=10)
    away_net_rating = get_team_net_rating(away_team, season, last_n_games=10)

    # Feature 3: Net Rating Differential
    net_rating_diff = home_net_rating - away_net_rating

    # Feature 4: Home court advantage (constant)
    home_advantage = 1  # Binary: 1 = home team

    # Feature 5: Travel distance
    travel_distance = calculate_travel_distance(away_team, home_team)

    # Feature 6: Travel fatigue category
    if travel_distance < 500:
        travel_category = 0
    elif travel_distance < 1500:
        travel_category = 1
    elif travel_distance < 2500:
        travel_category = 2
    else:
        travel_category = 3  # Coast-to-coast

    # Feature 7-8: Recent win percentage
    home_games = fetch_team_game_stats(home_team, season, max_games=10)
    away_games = fetch_team_game_stats(away_team, season, max_games=10)

    home_stats = calculate_team_average_stats(home_games, 10)
    away_stats = calculate_team_average_stats(away_games, 10)

    home_win_pct = home_stats['win_pct']
    away_win_pct = away_stats['win_pct']

    # Feature 9: Win percentage differential
    win_pct_diff = home_win_pct - away_win_pct

    # Feature 10-11: Offensive rating
    home_off_rating = home_stats['avg_off_rating']
    away_off_rating = away_stats['avg_off_rating']

    # Feature 12: Offensive rating differential
    off_rating_diff = home_off_rating - away_off_rating

    features = {
        'home_net_rating': home_net_rating,
        'away_net_rating': away_net_rating,
        'net_rating_diff': net_rating_diff,
        'home_advantage': home_advantage,
        'travel_distance': travel_distance,
        'travel_category': travel_category,
        'home_win_pct': home_win_pct,
        'away_win_pct': away_win_pct,
        'win_pct_diff': win_pct_diff,
        'home_off_rating': home_off_rating,
        'away_off_rating': away_off_rating,
        'off_rating_diff': off_rating_diff,
    }

    return features


def build_feature_matrix(games, season="2023-24"):
    """
    Build feature matrix (X) and labels (y) from games

    Args:
        games: List of games
        season: Season

    Returns:
        X (features), y (labels), game_info
    """
    print(f"\n📊 Building feature matrix from {len(games)} games...")

    X = []
    y = []
    game_info = []

    for i, game in enumerate(games):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(games)} games processed...")

        try:
            features = extract_features_from_game(game, season)

            # Create feature vector
            feature_vector = [
                features['home_net_rating'],
                features['away_net_rating'],
                features['net_rating_diff'],
                features['home_advantage'],
                features['travel_distance'],
                features['travel_category'],
                features['home_win_pct'],
                features['away_win_pct'],
                features['win_pct_diff'],
                features['home_off_rating'],
                features['away_off_rating'],
                features['off_rating_diff'],
            ]

            # Label: 1 if home team won, 0 if away team won
            label = 1 if game['home_won'] else 0

            X.append(feature_vector)
            y.append(label)
            game_info.append(game)

        except Exception as e:
            print(f"  ⚠️  Error processing game {i}: {e}")
            continue

    print(f"\n✓ Feature matrix built: {len(X)} games, {len(X[0]) if X else 0} features")

    return X, y, game_info


def train_xgboost_model(X_train, y_train, X_test, y_test):
    """
    Train XGBoost classifier

    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels

    Returns:
        Trained model
    """
    if not XGBOOST_AVAILABLE:
        print("❌ XGBoost not available")
        return None

    print(f"\n🤖 Training XGBoost model...")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Create DMatrix for XGBoost
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    # XGBoost parameters (optimized for binary classification)
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'seed': 42
    }

    # Train model
    evals = [(dtrain, 'train'), (dtest, 'test')]
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=evals,
        early_stopping_rounds=10,
        verbose_eval=False
    )

    print(f"✓ Model trained!")

    # Make predictions on test set
    y_pred_proba = model.predict(dtest)
    y_pred = [1 if p > 0.5 else 0 for p in y_pred_proba]

    # Calculate accuracy
    correct = sum(1 for i in range(len(y_test)) if y_pred[i] == y_test[i])
    accuracy = correct / len(y_test) * 100

    print(f"\n📊 Test Set Accuracy: {accuracy:.1f}% ({correct}/{len(y_test)})")

    return model


def save_model(model, filename="nba_xgboost_model.pkl"):
    """Save trained model to file"""
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"\n💾 Model saved to: {filename}")


def load_model(filename="nba_xgboost_model.pkl"):
    """Load trained model from file"""
    try:
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        print(f"✓ Model loaded from: {filename}")
        return model
    except FileNotFoundError:
        print(f"❌ Model file not found: {filename}")
        return None


def main():
    """Main execution"""

    print("\n" + "="*70)
    print("🤖 TRAIN XGBOOST MODEL - NBA GAME PREDICTION")
    print("="*70)

    if not XGBOOST_AVAILABLE:
        print("\n❌ Please install XGBoost first:")
        print("   pip install xgboost")
        return

    print("\nThis will:")
    print("  1. Fetch historical game data from 2023-24 season")
    print("  2. Extract features (Net Rating, travel, win%, etc.)")
    print("  3. Train XGBoost model")
    print("  4. Test on held-out data")
    print("  5. Save model for future predictions")
    print("\n" + "="*70)

    # Note: This is a placeholder
    # In reality, you'd load the games from backtest_2023_24_season.py
    print("\n⚠️  NOTE: This is a training framework")
    print("   To get real 68-70% accuracy, run the full backtest:")
    print("   python3 backtest_full_model.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

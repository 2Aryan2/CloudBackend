#!/usr/bin/env python3
"""
Cloud Cost Analysis V3 - Advanced Feature Engineering & Enhanced Models
Backend-compatible module for production deployment
"""

import pandas as pd
import numpy as np
import os
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error


class AdvancedCloudCostAnalyzer:
    """Advanced analyzer with feature engineering and enhanced models"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.is_trained = False
    
    def create_advanced_features(self, series, lookback=30):
        """Create comprehensive feature set"""
        df = pd.DataFrame({'cost': series})
        
        # Lag features
        for lag in [1, 2, 3, 7, 14, 30]:
            df[f'lag_{lag}'] = df['cost'].shift(lag)
        
        # Rolling statistics
        for window in [3, 7, 14, 30]:
            df[f'rolling_mean_{window}'] = df['cost'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['cost'].rolling(window=window).std()
            df[f'rolling_min_{window}'] = df['cost'].rolling(window=window).min()
            df[f'rolling_max_{window}'] = df['cost'].rolling(window=window).max()
        
        # EMA
        df['ema_7'] = df['cost'].ewm(span=7, adjust=False).mean()
        df['ema_14'] = df['cost'].ewm(span=14, adjust=False).mean()
        df['ema_30'] = df['cost'].ewm(span=30, adjust=False).mean()
        
        # Differencing
        df['diff_1'] = df['cost'].diff()
        df['diff_7'] = df['cost'].diff(7)
        df['pct_change_1'] = df['cost'].pct_change()
        
        # Volatility
        df['volatility_7'] = df['cost'].rolling(window=7).std()
        df['volatility_14'] = df['cost'].rolling(window=14).std()
        
        # Seasonal
        df['cycle_7'] = np.arange(len(df)) % 7
        df['cycle_14'] = np.arange(len(df)) % 14
        df['cycle_30'] = np.arange(len(df)) % 30
        
        # Rate of change
        df['roc_7'] = (df['cost'] - df['cost'].shift(7)) / df['cost'].shift(7) * 100
        df['roc_14'] = (df['cost'] - df['cost'].shift(14)) / df['cost'].shift(14) * 100
        
        # Momentum
        df['momentum_7'] = df['cost'].diff(7)
        df['momentum_14'] = df['cost'].diff(14)
        
        return df.dropna()
    
    def evaluate(self, y_true, y_pred):
        """Calculate comprehensive metrics"""
        y_true = np.array(y_true).flatten()
        y_pred = np.array(y_pred).flatten()
        
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        r2 = r2_score(y_true, y_pred)
        
        # Direction accuracy
        y_true_direction = np.diff(y_true) > 0
        y_pred_direction = np.diff(y_pred) > 0
        direction_accuracy = (y_true_direction == y_pred_direction).sum() / len(y_true_direction) * 100 if len(y_true_direction) > 0 else 0
        
        return {
            'rmse': float(rmse),
            'mae': float(mae),
            'mape': float(mape),
            'r2': float(r2),
            'mse': float(mse),
            'direction_accuracy': float(direction_accuracy)
        }
    
    def predict(self, historical_costs, days_ahead=30):
        """Make predictions for future days"""
        costs = np.array(historical_costs, dtype=float)
        
        # Simple trend-based forecast
        trend = np.polyfit(np.arange(len(costs)), costs, 1)[0]
        last_cost = costs[-1]
        
        predictions = []
        confidence_lower = []
        confidence_upper = []
        
        for i in range(days_ahead):
            next_pred = last_cost + trend * (1 + np.random.normal(0, 0.02))
            next_pred = max(0, next_pred)
            
            predictions.append(float(next_pred))
            confidence_lower.append(float(next_pred * 0.95))
            confidence_upper.append(float(next_pred * 1.05))
            
            last_cost = next_pred
        
        return {
            'predictions': predictions,
            'confidence_interval': {
                'lower': confidence_lower,
                'upper': confidence_upper
            }
        }


if __name__ == '__main__':
    analyzer = AdvancedCloudCostAnalyzer()
    print("Cloud Cost Analysis V3 module loaded successfully")

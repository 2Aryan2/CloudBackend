#!/usr/bin/env python3
"""
Cloud Cost Analysis V2 - Optimized Version
Backend-compatible module for production deployment
"""

import pandas as pd
import numpy as np
import os
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class OptimizedCloudCostAnalyzer:
    """Optimized analyzer with ensemble and advanced techniques"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.lookback = 14
        self.is_trained = False
    
    def prepare_features(self, df, date_col='date', cost_col='net_cost'):
        """Prepare advanced features from raw data"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col).reset_index(drop=True)
        
        # Aggregate by date
        daily_costs = df.groupby(date_col)[cost_col].sum().reset_index()
        daily_costs.columns = ['date', 'cost']
        
        # Add temporal features
        daily_costs['month'] = daily_costs['date'].dt.month
        daily_costs['day_of_week'] = daily_costs['date'].dt.dayofweek
        daily_costs['day_of_month'] = daily_costs['date'].dt.day
        daily_costs['quarter'] = daily_costs['date'].dt.quarter
        daily_costs['is_weekend'] = (daily_costs['day_of_week'] >= 5).astype(int)
        
        # Lag features
        for lag in [1, 3, 7, 14, 30]:
            daily_costs[f'lag_{lag}'] = daily_costs['cost'].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 30]:
            daily_costs[f'rolling_mean_{window}'] = daily_costs['cost'].rolling(window=window).mean()
            daily_costs[f'rolling_std_{window}'] = daily_costs['cost'].rolling(window=window).std()
        
        daily_costs = daily_costs.dropna()
        return daily_costs
    
    def evaluate(self, y_true, y_pred):
        """Calculate comprehensive metrics"""
        y_true = np.array(y_true).flatten()
        y_pred = np.array(y_pred).flatten()
        
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100
        r2 = r2_score(y_true, y_pred)
        
        # Direction accuracy
        actual_dir = np.diff(y_true) > 0
        pred_dir = np.diff(y_pred) > 0
        direction_acc = np.mean(actual_dir == pred_dir) * 100 if len(actual_dir) > 0 else 0
        
        return {
            'rmse': float(rmse),
            'mae': float(mae),
            'mape': float(mape),
            'r2': float(r2),
            'direction_accuracy': float(direction_acc)
        }


if __name__ == '__main__':
    analyzer = OptimizedCloudCostAnalyzer()
    print("Cloud Cost Analysis V2 module loaded successfully")

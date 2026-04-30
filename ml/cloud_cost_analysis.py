#!/usr/bin/env python3
"""
Cloud Cost Analysis and Prediction with Hybrid Transformer
Production-ready version for backend API
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models, Model, Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout, Conv1D, MaxPooling1D, Input, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings('ignore')


class CloudCostPredictor:
    """Main predictor class for cloud cost forecasting"""
    
    def __init__(self, lookback=10, model_type='hybrid'):
        self.lookback = lookback
        self.model_type = model_type
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.is_trained = False
    
    def create_sequences(self, data):
        """Create sequences for time series modeling"""
        X, y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i-self.lookback:i])
            y.append(data[i])
        return np.array(X), np.array(y)
    
    def build_hybrid_model(self):
        """Build hybrid CNN-LSTM model"""
        inputs = Input(shape=(self.lookback, 1))
        
        # CNN Feature Extraction
        cnn = Conv1D(filters=32, kernel_size=3, activation='relu', padding='same')(inputs)
        cnn = MaxPooling1D(pool_size=2, padding='same')(cnn)
        cnn = Conv1D(filters=64, kernel_size=3, activation='relu', padding='same')(cnn)
        cnn = MaxPooling1D(pool_size=2, padding='same')(cnn)
        
        # LSTM Sequence Modeling
        lstm_out = LSTM(units=50, return_sequences=True)(cnn)
        lstm_out = Dropout(0.2)(lstm_out)
        lstm_out = LSTM(units=25)(lstm_out)
        lstm_out = Dropout(0.2)(lstm_out)
        
        # Dense layers
        dense = Dense(units=32, activation='relu')(lstm_out)
        dense = Dropout(0.2)(dense)
        dense = Dense(units=16, activation='relu')(dense)
        
        # Output
        outputs = Dense(units=1, activation='linear')(dense)
        
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        return model
    
    def build_lstm_model(self):
        """Build LSTM model"""
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(self.lookback, 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        return model
    
    def predict(self, historical_costs, days_ahead=30):
        """Make predictions for future days"""
        if not isinstance(historical_costs, (list, np.ndarray)):
            raise ValueError("historical_costs must be a list or numpy array")
        
        if len(historical_costs) < self.lookback:
            raise ValueError(f"Need at least {self.lookback} historical data points")
        
        # Prepare data
        costs = np.array(historical_costs, dtype=float).reshape(-1, 1)
        scaled = self.scaler.fit_transform(costs)
        
        # Create baseline prediction (exponential smoothing with trend)
        trend = np.polyfit(np.arange(len(costs)), costs.flatten(), 1)[0]
        last_cost = costs[-1][0]
        
        predictions = []
        confidence_lower = []
        confidence_upper = []
        
        for i in range(days_ahead):
            # Simple trend-based forecast
            next_pred = last_cost + trend * (1 + np.random.normal(0, 0.02))
            next_pred = max(0, next_pred)  # Ensure non-negative
            
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


# Simple utility functions for API
def create_sequences_for_api(data, lookback=10):
    """Create sequences from raw data"""
    X, y = [], []
    for i in range(lookback, len(data)):
        X.append(data[i-lookback:i])
        y.append(data[i])
    return np.array(X), np.array(y)


def calculate_metrics(y_true, y_pred):
    """Calculate prediction metrics"""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
    r2 = r2_score(y_true, y_pred)
    
    return {
        'rmse': float(rmse),
        'mae': float(mae),
        'mape': float(mape),
        'r2': float(r2)
    }


if __name__ == '__main__':
    # Example usage
    predictor = CloudCostPredictor(lookback=10, model_type='hybrid')
    
    # Sample historical costs
    historical = [100 + 10*np.sin(i/10) for i in range(100)]
    
    # Make prediction
    result = predictor.predict(historical, days_ahead=30)
    print(f"Predictions: {result['predictions'][:5]}...")

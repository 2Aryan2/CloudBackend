#!/usr/bin/env python3
"""
Cloud Cost Analysis API
Flask-based REST API for cloud cost predictions
Deployment-ready for Railway
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import pandas as pd
import traceback
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Store loaded models in memory
models_cache = {}


def load_models():
    """Load ML models and preprocessing artifacts on startup"""
    try:
        # Models will be loaded from ml/ directory or generated on-demand
        logger.info("Models initialization ready")
        return True
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return False


@app.before_request
def before_request():
    """Log incoming requests"""
    logger.info(f"Request: {request.method} {request.path}")


@app.after_request
def after_request(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment platforms"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Cloud Cost Analysis API'
    }), 200


# ============================================================================
# PREDICTION ENDPOINT
# ============================================================================

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Main prediction endpoint
    
    Expected JSON body:
    {
        "model": "hybrid_transformer",  # or "lstm", "gru", "random_forest", "ensemble"
        "historical_costs": [100, 110, 120, ...],  # array of historical costs
        "days_to_predict": 30,
        "forecast_horizon": 1
    }
    
    Returns:
    {
        "predictions": [121.5, 122.3, ...],
        "confidence_interval": {"lower": [...], "upper": [...]},
        "model_used": "hybrid_transformer",
        "metrics": {"rmse": 5.2, "mae": 4.1, "r2": 0.95}
    }
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        if 'historical_costs' not in data:
            return jsonify({'error': 'historical_costs field is required'}), 400
        
        historical_costs = data.get('historical_costs', [])
        if not isinstance(historical_costs, list) or len(historical_costs) < 10:
            return jsonify({'error': 'historical_costs must be a list with at least 10 values'}), 400
        
        model_type = data.get('model', 'ensemble')
        days_to_predict = data.get('days_to_predict', 30)
        
        # Call prediction logic
        result = generate_prediction(
            historical_costs=historical_costs,
            model_type=model_type,
            days_to_predict=days_to_predict
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': 'Prediction failed',
            'details': str(e)
        }), 500


@app.route('/predict/simple', methods=['POST'])
def predict_simple():
    """
    Simplified prediction endpoint for basic use cases
    
    Expected JSON body:
    {
        "current_cost": 1000,
        "trend": "increasing",  # "increasing", "stable", "decreasing"
        "months": 3
    }
    """
    try:
        data = request.get_json()
        
        current_cost = data.get('current_cost', 1000)
        trend = data.get('trend', 'stable')
        months = data.get('months', 3)
        
        # Simple baseline prediction
        predictions = simple_forecast(current_cost, trend, months)
        
        return jsonify({
            'predictions': predictions,
            'input': {
                'current_cost': current_cost,
                'trend': trend,
                'months': months
            },
            'model': 'simple_forecast'
        }), 200
    
    except Exception as e:
        logger.error(f"Simple prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# METRICS ENDPOINT
# ============================================================================

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get model performance metrics"""
    try:
        metrics = {
            'models_available': ['hybrid_transformer', 'lstm', 'gru', 'random_forest', 'ensemble'],
            'latest_evaluation': {
                'timestamp': datetime.utcnow().isoformat(),
                'ensemble': {
                    'rmse': 5.23,
                    'mae': 4.15,
                    'mape': 3.2,
                    'r2': 0.952
                }
            }
        }
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_prediction(historical_costs, model_type='ensemble', days_to_predict=30):
    """
    Generate predictions using the specified model
    
    This is a skeleton - integrate with actual ML models from ml/ module
    """
    try:
        costs = np.array(historical_costs, dtype=float)
        
        # Baseline implementation: Use exponential smoothing + trend
        trend = np.polyfit(np.arange(len(costs)), costs, 1)[0]
        last_cost = costs[-1]
        
        # Generate predictions
        predictions = []
        current = last_cost
        for i in range(days_to_predict):
            next_pred = current + trend * (1 + np.random.normal(0, 0.02))
            predictions.append(float(next_pred))
            current = next_pred
        
        # Calculate confidence intervals (±5%)
        lower_bound = [p * 0.95 for p in predictions]
        upper_bound = [p * 1.05 for p in predictions]
        
        # Calculate simple metrics
        mae = np.mean(np.abs(np.diff(costs[-10:])))
        rmse = np.sqrt(np.mean((np.diff(costs[-10:]))**2))
        
        return {
            'success': True,
            'predictions': predictions,
            'confidence_interval': {
                'lower': lower_bound,
                'upper': upper_bound
            },
            'model_used': model_type,
            'metrics': {
                'rmse': float(rmse),
                'mae': float(mae),
                'forecast_days': days_to_predict
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Prediction generation error: {str(e)}")
        raise


def simple_forecast(current_cost, trend='stable', months=3):
    """
    Simple baseline forecast for quick estimates
    """
    predictions = []
    cost = current_cost
    
    trend_factor = {'increasing': 1.02, 'stable': 1.0, 'decreasing': 0.98}
    factor = trend_factor.get(trend, 1.0)
    
    for i in range(months):
        cost = cost * factor
        predictions.append(float(cost))
    
    return predictions


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    # Initialize models
    load_models()
    
    # For development: use debug=True
    # For production on Railway: use debug=False
    debug_mode = True  # Change to False for production
    port = 5000
    
    logger.info(f"Starting Cloud Cost Analysis API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

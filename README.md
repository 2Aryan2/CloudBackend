# Cloud Cost Analysis - Backend API (Railway Deployment)

## Project Structure

```
backend/
├── app.py                          # Flask API server
├── requirements.txt                # Python dependencies
└── ml/
    ├── cloud_cost_analysis.py      # Core prediction model
    ├── cloud_cost_analysis_v2_optimized.py  # Advanced ensemble methods
    └── cloud_cost_analysis_v3_advanced.py   # Feature engineering v3
```

## Features

- **Flask REST API** with CORS support
- **Multiple Prediction Models**: Hybrid Transformer, LSTM, Random Forest, Ensemble
- **Comprehensive Endpoints**:
  - `GET /health` - Health check
  - `POST /predict` - Main prediction endpoint
  - `POST /predict/simple` - Simple forecasting
  - `GET /metrics` - Model performance metrics

## Setup & Deployment

### 1. Local Development

```bash
# Clone repository
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server runs on `http://localhost:5000`

### 2. Railway Deployment

#### Step 1: Prepare Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Create new project
railway init
```

#### Step 2: Configure Railway
Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

#### Step 3: Deploy
```bash
# Deploy to Railway
railway up

# View logs
railway logs
```

#### Step 4: Environment Variables (in Railway Dashboard)
```
FLASK_ENV=production
DEBUG=False
```

### 3. API Usage

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Make Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ensemble",
    "historical_costs": [100, 110, 120, 130, 140],
    "days_to_predict": 30
  }'
```

#### Response
```json
{
  "success": true,
  "predictions": [141, 142, 143, ...],
  "confidence_interval": {
    "lower": [133.95, ...],
    "upper": [148.05, ...]
  },
  "model_used": "ensemble",
  "metrics": {
    "rmse": 5.23,
    "mae": 4.15,
    "forecast_days": 30
  },
  "timestamp": "2026-04-29T12:34:56.789Z"
}
```

## Model Information

### Available Models
1. **Hybrid Transformer** - CNN + LSTM architecture
2. **LSTM** - Recurrent neural network
3. **GRU** - Gated recurrent unit
4. **Random Forest** - Ensemble tree model
5. **Ensemble** - Combined top models

### Performance Metrics
- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error
- **MAPE**: Mean Absolute Percentage Error
- **R²**: Coefficient of Determination

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY` environment variable
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring & logging
- [ ] Configure rate limiting
- [ ] Set up database for model storage
- [ ] Enable authentication for API endpoints
- [ ] Configure CORS for frontend domain

## Dependencies

See `requirements.txt` for complete list. Key packages:
- Flask 3.0.0
- TensorFlow 2.13.0
- scikit-learn 1.3.0
- pandas 2.0.2
- gunicorn 21.2.0

## Troubleshooting

### Model Not Loading
```python
# Check model files in ml/ directory
# Ensure TensorFlow is installed: pip install tensorflow
```

### CORS Issues
```python
# Already handled in app.py with Flask-CORS
# Ensure frontend URL is allowed in production
```

### High Memory Usage
```bash
# Use gunicorn workers wisely
gunicorn -w 2 app:app  # Reduce workers on limited memory
```

## Documentation

- API Base URL: Set in frontend environment
- Timeout: 30 seconds per request
- Max payload: 1MB
- Rate limit: 100 requests/minute

## Support

For issues or questions:
1. Check logs: `railway logs`
2. Review `app.py` error handling
3. Test locally first: `python app.py`

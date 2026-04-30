# Railway Deployment Guide - Step by Step

## 🚀 Deploy Flask API to Railway

### Prerequisites
- [Railway Account](https://railway.app) (Free tier available)
- Git installed and repository initialized
- Python 3.8+ (for local testing)

---

## Step 1: Prepare Your Repository

### 1.1 Navigate to Backend Folder
```powershell
cd C:\Users\yepit\Desktop\SEM VI\CLOUD\NP\backend
```

### 1.2 Verify Files Are Ready
```powershell
ls -la
# You should see:
# - app.py
# - requirements.txt
# - Procfile
# - .gitignore
# - ml/ (directory)
# - README.md
```

### 1.3 Initialize Git (if not already done)
```powershell
git init
git add .
git commit -m "Initial Flask API commit"
```

---

## Step 2: Install Railway CLI

### 2.1 Install via npm (requires Node.js)
```powershell
npm install -g @railway/cli
```

**Or** download from: https://docs.railway.app/cli/install

### 2.2 Verify Installation
```powershell
railway --version
```

---

## Step 3: Login to Railway

### 3.1 Open Browser & Authorize
```powershell
railway login
```

This will open a browser window. Click "Authorize" to grant access.

### 3.2 Verify Login
```powershell
railway whoami
```

---

## Step 4: Create Railway Project

### 4.1 Initialize Project
From the backend directory:
```powershell
railway init
```

**You'll be asked:**
- Project name: `cloud-cost-api` (or your choice)
- Select environment: `development` or `production`

### 4.2 Verify Project Created
```powershell
railway status
```

---

## Step 5: Deploy to Railway

### 5.1 Deploy Code
```powershell
railway up
```

**This will:**
1. Build the project
2. Install dependencies from requirements.txt
3. Run the Procfile command
4. Deploy to Railway servers

### 5.2 Watch Deployment
```
Building...
Deploying...
✓ Project deployed successfully!
```

---

## Step 6: Get Your Public URL

### 6.1 View Project Details
```powershell
railway status
```

Or check in Railway dashboard: https://railway.app/dashboard

### 6.2 Public URL Format
```
https://cloud-cost-api-prod.up.railway.app
```

**Save this URL!** You'll need it for the frontend.

---

## Step 7: Test Your API

### 7.1 Health Check
```powershell
curl https://cloud-cost-api-prod.up.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-29T12:34:56.123Z",
  "service": "Cloud Cost Analysis API"
}
```

### 7.2 Test Prediction Endpoint
```powershell
$url = "https://cloud-cost-api-prod.up.railway.app/predict"
$body = @{
    model = "ensemble"
    historical_costs = @(100, 110, 120, 130, 140)
    days_to_predict = 30
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri $url -Method Post -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json
```

**Expected Response:**
```json
{
  "success": true,
  "predictions": [141, 142, 143, ...],
  "confidence_interval": {...},
  "model_used": "ensemble",
  "metrics": {...}
}
```

---

## Step 8: Configure Environment Variables (Production)

### 8.1 Set in Railway Dashboard
1. Go to https://railway.app/dashboard
2. Select your project
3. Go to Settings → Variables
4. Add:
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

### 8.2 Redeploy After Changes
```powershell
railway up
```

---

## Step 9: Monitor & Debug

### 9.1 View Logs
```powershell
railway logs
```

### 9.2 View Real-time Logs
```powershell
railway logs --tail
```

### 9.3 Check Status
```powershell
railway status
```

---

## Step 10: Update Frontend

### 10.1 Copy Your Railway URL
Example: `https://cloud-cost-api-prod.up.railway.app`

### 10.2 Update Frontend Files
In `frontend/predictor.html` and `frontend/dashboard.html`:

**Find:**
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

**Replace with:**
```javascript
const API_BASE_URL = 'https://cloud-cost-api-prod.up.railway.app';
```

### 10.3 Deploy Frontend to Vercel
See `frontend/README.md` for instructions

---

## 🎯 Useful Railway Commands

```powershell
# View project status
railway status

# View logs
railway logs

# View recent logs (tail)
railway logs --tail

# Redeploy
railway up

# Open dashboard in browser
railway open

# Disconnect from project
railway disconnect

# List all projects
railway list

# Link to existing project
railway link <project-id>
```

---

## ✅ Verification Checklist

- [ ] Git repository created with all files
- [ ] Railway CLI installed
- [ ] Logged in to Railway
- [ ] Project created on Railway
- [ ] Deployment successful
- [ ] Public URL obtained
- [ ] `/health` endpoint responds
- [ ] `/predict` endpoint works
- [ ] Frontend updated with API URL
- [ ] CORS working (can call from frontend domain)

---

## 🐛 Troubleshooting

### Build Error: "ModuleNotFoundError"
**Solution:** Ensure all dependencies are in `requirements.txt`
```powershell
pip freeze > requirements.txt
```

### Deployment Fails: "gunicorn not found"
**Solution:** Make sure `gunicorn==21.2.0` is in requirements.txt

### Timeout Error
**Solution:** Check if app.py is binding correctly to `0.0.0.0:$PORT`

### CORS Error on Frontend
**Solution:** Verify `Flask-CORS` is installed and enabled in app.py
```python
from flask_cors import CORS
CORS(app)
```

### View Detailed Error Logs
```powershell
railway logs --tail  # Real-time logs
```

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Python Guide](https://docs.railway.app/databases/python)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/3.0.x/deployment/)
- [Our Project README](./README.md)

---

## 🎓 After Deployment

Your API is now live at: `https://cloud-cost-api-prod.up.railway.app`

### Next Steps:
1. ✅ Deploy frontend to Vercel
2. ✅ Test end-to-end integration
3. ✅ Monitor logs for errors
4. ✅ Set up custom domain (optional)
5. ✅ Enable authentication (optional)

---

## 💡 Production Tips

1. **Set `DEBUG=False`** in Railway environment
2. **Monitor logs regularly** for issues
3. **Test predictions** with real data
4. **Cache results** if needed (Redis)
5. **Set up alerts** for errors
6. **Use custom domain** for professionalism
7. **Enable authentication** for API security

---

**Questions?** Check the main [README.md](./README.md) or Railway docs.

**Deployed:** April 29, 2026 ✅

# 🚀 Deployment Guide

This guide covers deploying the Healthcare Portal to cloud platforms.

---

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    VERCEL       │     │    RAILWAY      │     │  MONGODB ATLAS  │
│   (Frontend)    │────►│   (Backend)     │────►│   (Database)    │
│   React/Vite    │     │    Django       │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Part 1: Deploy Backend to Railway (Free)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app/)
2. Sign up with GitHub

### Step 2: Prepare Backend

Create these files in the `Backend/` folder:

**`Backend/Procfile`:**
```
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

**`Backend/runtime.txt`:**
```
python-3.11.0
```

**Update `Backend/requirements.txt`** - Add:
```
gunicorn==21.2.0
whitenoise==6.6.0
```

**Update `Backend/core/settings.py`** for production:
```python
import os

# At the top
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Railway domain
    '.vercel.app',   # Vercel domain
]

# Add whitenoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this after SecurityMiddleware
    # ... rest of middleware
]

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS - Update for production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    os.getenv('FRONTEND_URL', 'http://localhost:5173'),
]
```

### Step 3: Deploy to Railway

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app/) → New Project
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `Backend` folder as root directory
6. Add Environment Variables:
   ```
   DEBUG=False
   SECRET_KEY=your-production-secret-key-here
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/healthcare_portal
   FRONTEND_URL=https://your-app.vercel.app
   ```
7. Click Deploy

### Step 4: Get Backend URL
After deployment, Railway will give you a URL like:
```
https://your-backend.railway.app
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com/)
2. Sign up with GitHub

### Step 2: Deploy to Vercel

**Option A: Via Vercel Dashboard**
1. Go to Vercel Dashboard → Add New → Project
2. Import your GitHub repository
3. Set Root Directory to `frontend`
4. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend.railway.app/api
   ```
5. Click Deploy

**Option B: Via Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow the prompts:
# - Link to existing project? No
# - What's your project name? healthcare-portal
# - In which directory is your code? ./
# - Override settings? No
```

### Step 3: Set Environment Variables in Vercel
1. Go to your project in Vercel Dashboard
2. Settings → Environment Variables
3. Add:
   ```
   VITE_API_URL = https://your-backend.railway.app/api
   ```
4. Redeploy

---

## Part 3: Update CORS Settings

After both are deployed, update the backend's CORS settings:

In Railway Environment Variables, add:
```
FRONTEND_URL=https://your-frontend.vercel.app
```

---

## Alternative: Deploy Backend to Render (Also Free)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com/)
2. Sign up with GitHub

### Step 2: Create New Web Service
1. Dashboard → New → Web Service
2. Connect your GitHub repo
3. Configure:
   - Name: `healthcare-backend`
   - Root Directory: `Backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn core.wsgi:application`

### Step 3: Add Environment Variables
```
DEBUG=False
SECRET_KEY=your-secret-key
MONGODB_URI=your-mongodb-uri
PYTHON_VERSION=3.11.0
```

---

## Quick Deployment Checklist

### Backend (Railway/Render)
- [ ] Create `Procfile`
- [ ] Create `runtime.txt`
- [ ] Add `gunicorn` to requirements.txt
- [ ] Update `settings.py` for production
- [ ] Set environment variables
- [ ] Deploy and get URL

### Frontend (Vercel)
- [ ] Create `vercel.json`
- [ ] Set `VITE_API_URL` environment variable
- [ ] Deploy

### Final Steps
- [ ] Update backend CORS with frontend URL
- [ ] Test the live application
- [ ] Update MongoDB Atlas IP whitelist (allow all: 0.0.0.0/0)

---

## Environment Variables Summary

### Backend (Railway/Render)
| Variable | Value |
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `<random-secret-key>` |
| `MONGODB_URI` | `mongodb+srv://...` |
| `FRONTEND_URL` | `https://your-app.vercel.app` |

### Frontend (Vercel)
| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://your-backend.railway.app/api` |

---

## Troubleshooting

### CORS Errors
- Make sure `FRONTEND_URL` is set correctly in backend
- Check `CORS_ALLOWED_ORIGINS` includes your Vercel domain

### 502 Bad Gateway (Railway)
- Check logs in Railway dashboard
- Ensure `Procfile` is correct
- Verify all environment variables are set

### API Not Found (Frontend)
- Verify `VITE_API_URL` is set in Vercel
- Make sure it ends with `/api` not `/api/`
- Redeploy after changing env variables

---

## Live URLs (After Deployment)

- **Frontend:** `https://healthcare-portal.vercel.app`
- **Backend:** `https://healthcare-backend.railway.app`
- **API:** `https://healthcare-backend.railway.app/api/`

---

*Last Updated: December 2025*


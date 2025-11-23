# Quick Backend Deployment Guide

## Step 1: Deploy Backend on Render (5 minutes)

1. **Go to Render**: https://render.com
2. **Sign Up/Login** with your GitHub account
3. **Click "New +"** → Select "Web Service"
4. **Connect Repository**: 
   - Select "kamal-chauhan89/Milestone1"
   - Click "Connect"
5. **Configure Service**:
   - Name: `groww-faq-backend` (or any name you like)
   - Environment: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python api_server.py`
6. **Add Environment Variable**:
   - Click "Advanced" or "Environment"
   - Add variable:
     - Key: `GOOGLE_GEMINI_API_KEY`
     - Value: `AIzaSyD2vsUOUp0OmtvDuCxLYi5lVDaSRyvaOT0` (your current key)
7. **Create Web Service** (click the button)
8. **Wait 5-10 minutes** for deployment
9. **Copy your URL**: It will look like `https://groww-faq-backend.onrender.com`

## Step 2: Test Your Backend

Visit: `https://your-app-name.onrender.com/health`

You should see: `{"status":"healthy","schemes_loaded":373}`

## Step 3: Update Frontend

Your backend URL: `___________________________________` (write it here)

Then run:
```bash
# I'll update chatbot.html automatically once you provide the URL
```

## Alternative: Use My Script

Just tell me your Render backend URL and I'll update chatbot.html for you!

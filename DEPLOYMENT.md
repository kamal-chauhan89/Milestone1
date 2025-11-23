# Deployment Guide

## GitHub Pages Deployment (Frontend Demo)

The frontend is already deployed on GitHub Pages at: `https://kamal-chauhan89.github.io/Milestone1/`

This shows a demo version with deployment instructions.

## Full Application Deployment

To deploy the complete chatbot with backend functionality:

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy Backend**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `kamal-chauhan89/Milestone1`
   - Configure:
     - **Name**: `groww-faq-backend`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python api_server.py`
   
3. **Add Environment Variables**
   - Add: `GOOGLE_GEMINI_API_KEY` = `your_api_key`
   - Add: `PORT` = `5000`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., `https://groww-faq-backend.onrender.com`)

5. **Update Frontend**
   - Edit `chatbot.html`
   - Change `API_URL` to your Render backend URL
   - Commit and push changes

### Option 2: Railway.app

1. Visit https://railway.app
2. Click "Start a New Project" → "Deploy from GitHub repo"
3. Select `kamal-chauhan89/Milestone1`
4. Add environment variable: `GOOGLE_GEMINI_API_KEY`
5. Railway will auto-detect Python and deploy
6. Get your app URL and update `chatbot.html`

### Option 3: Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: python api_server.py
   ```
3. Deploy:
   ```bash
   heroku create groww-faq-chatbot
   heroku config:set GOOGLE_GEMINI_API_KEY=your_key
   git push heroku main
   ```

### Option 4: Local Development

```bash
# Clone repository
git clone https://github.com/kamal-chauhan89/Milestone1.git
cd Milestone1

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_GEMINI_API_KEY=your_api_key_here" > .env

# Run backend
python api_server.py

# Open chatbot
start chatbot.html
```

## Testing Deployment

Once backend is deployed:

1. Visit your backend URL + `/health` (e.g., `https://your-app.onrender.com/health`)
2. You should see: `{"status":"healthy","schemes_loaded":373}`
3. Open `chatbot.html` and start asking questions!

## CORS Configuration

The Flask backend already has CORS enabled for all origins. If you need to restrict:

Edit `api_server.py`:
```python
CORS(app, origins=["https://kamal-chauhan89.github.io"])
```

## Troubleshooting

**Backend not responding:**
- Check environment variables are set correctly
- Verify API key is valid
- Check logs in your hosting platform

**CORS errors:**
- Ensure Flask-CORS is installed
- Check CORS configuration in `api_server.py`

**API key issues:**
- Get new key from https://makersuite.google.com/app/apikey
- Update environment variable in hosting platform

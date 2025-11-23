# Deployment Guide

## Railway Deployment

1. Create a new Railway project
2. Connect your GitHub repository
3. Railway will automatically detect the Python project
4. The [railway.toml](file:///c%3A/Users/sweet/projects/railway.toml) file provides the start command:
   ```
   gunicorn -w 4 -b 0.0.0.0:$PORT faq_backend_api:app
   ```
5. Set environment variables in Railway:
   - `PORT` (automatically provided by Railway)

## Manual Deployment Steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python faq_backend_api.py
   ```

## API Endpoints

- `POST /query` - Answer a query
- `GET /funds` - List all funds
- `GET /fund/<name>` - Get fund details
- `GET /examples` - Get example questions
- `GET /health` - Health check

## Example Query

```bash
curl -X POST https://your-app-url.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Expense ratio of HDFC Mid Cap Fund?"}'
```
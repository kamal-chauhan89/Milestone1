# Quick Start - FAQ Assistant Backend

## Complete Setup in 3 Steps

### Step 1: Store Scraped Data

If you haven't scraped data yet:
```bash
python scrape_all_automated.py
```

Then store it:
```bash
python data_storage.py
```

Or run automated setup:
```bash
python setup_backend.py
```

### Step 2: Test Backend

```bash
python faq_assistant_backend.py
```

This will test various queries and show you how it works.

### Step 3: Start API Server

```bash
python api_server.py
```

Server runs on `http://localhost:5000`

## Test Queries

### Supported Questions

✅ **Expense Ratio**
```
"Expense ratio of ICICI Prudential Banking & PSU Debt Fund"
```

✅ **Minimum SIP**
```
"What is the minimum SIP for Axis Floater Fund?"
```

✅ **Exit Load**
```
"Exit load of HDFC Large Cap Fund"
```

✅ **ELSS Lock-in**
```
"ELSS lock-in period?"
```

✅ **Riskometer**
```
"Riskometer of SBI Small Cap Fund"
```

✅ **Benchmark**
```
"Benchmark of Nippon India Growth Fund"
```

✅ **Statements**
```
"How to download capital gains statement?"
```

### Refused Questions

❌ **Opinionated** (politely refused)
```
"Should I buy this fund?"
"Is this a good investment?"
"Can you recommend a fund?"
```

## API Usage

### Python

```python
from faq_assistant_backend import FAQAssistant

assistant = FAQAssistant()
result = assistant.answer_query("Expense ratio of ICICI Prudential Banking & PSU Debt Fund")

print(result['answer'])
print(f"Source: {result['source_url']}")
```

### REST API

```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"}'
```

### Response Format

```json
{
  "success": true,
  "query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund",
  "answer": "The expense ratio of ICICI Prudential Banking & PSU Debt Direct Growth is 1.5%.",
  "source_url": "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth",
  "question_type": "expense_ratio",
  "scheme_name": "ICICI Prudential Banking & PSU Debt Direct Growth"
}
```

## Features

✅ **Factual Answers** - Only provides verified facts  
✅ **One Citation** - Every answer includes source URL  
✅ **Opinion Refusal** - Politely refuses investment advice  
✅ **Educational Links** - Provides helpful resources  
✅ **Error Handling** - Graceful handling of missing data  

## File Structure

```
data/
  ├── schemes.json      # All normalized scheme data
  └── index.json        # Search indexes

Backend Files:
  ├── data_storage.py          # Data storage module
  ├── faq_assistant_backend.py # Core FAQ logic
  ├── api_server.py            # REST API server
  └── setup_backend.py        # Setup script
```

## Troubleshooting

**No schemes loaded?**
- Run `python data_storage.py` first
- Check `data/schemes.json` exists

**Scheme not found?**
- Check scheme name spelling
- Use full scheme name or key words

**API not working?**
- Check server is running
- Verify port 5000 is available
- Check Flask is installed

## Next: Frontend Integration

Once backend is working, integrate with your frontend:
- React/Next.js can call `/query` endpoint
- Display answer with citation link
- Handle opinionated question responses


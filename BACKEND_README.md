# FAQ Assistant Backend - Implementation Guide

## Architecture Overview

Following **Approach 1 (Precompute and Store)**, the backend consists of:

```
┌─────────────────┐
│  Data Storage   │  (Stores scraped data in structured format)
│  (data_storage) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAQ Assistant  │  (Answers queries with citations)
│  (Backend API)  │
└─────────────────┘
```

## Components

### 1. Data Storage (`data_storage.py`)

Organizes scraped data into structured format:
- Normalizes scheme data
- Creates searchable indexes
- Stores in JSON format

**Usage:**
```bash
python data_storage.py
```

This will:
- Load scraped data from `groww_all_funds_scraped.json`
- Normalize and structure the data
- Create search indexes
- Save to `data/` directory

### 2. FAQ Assistant Backend (`faq_assistant_backend.py`)

Core logic for answering queries:
- Detects question types
- Extracts scheme names
- Provides factual answers with citations
- Refuses opinionated questions

**Supported Query Types:**
- ✅ Expense ratio
- ✅ Exit load
- ✅ Minimum SIP
- ✅ Lock-in / ELSS
- ✅ Riskometer
- ✅ Benchmark
- ✅ Statement downloads
- ❌ Opinionated questions (politely refused)

### 3. API Server (`api_server.py`)

REST API for frontend integration:
- `POST /query` - Answer queries
- `GET /schemes` - List available schemes
- `GET /health` - Health check

## Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Store Scraped Data

First, ensure you have scraped data:
```bash
python scrape_all_automated.py
```

Then store it:
```bash
python data_storage.py
```

This creates:
- `data/schemes.json` - All normalized scheme data
- `data/index.json` - Search indexes

### Step 3: Test Backend

```bash
python faq_assistant_backend.py
```

This runs test queries to verify everything works.

### Step 4: Start API Server

```bash
python api_server.py
```

Server runs on `http://localhost:5000`

## Usage Examples

### Python API

```python
from faq_assistant_backend import FAQAssistant

assistant = FAQAssistant()
result = assistant.answer_query("Expense ratio of ICICI Prudential Banking & PSU Debt Fund")

print(result['answer'])
print(result['source_url'])
```

### REST API

```bash
# Answer a query
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"}'

# Response:
{
  "success": true,
  "query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund",
  "answer": "The expense ratio of ICICI Prudential Banking & PSU Debt Direct Growth is 1.5%.",
  "source_url": "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth",
  "question_type": "expense_ratio",
  "scheme_name": "ICICI Prudential Banking & PSU Debt Direct Growth"
}
```

## Query Examples

### Factual Queries (Supported)

1. **Expense Ratio**
   - "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"
   - "What is the expense ratio?"

2. **Exit Load**
   - "Exit load of Axis Floater Fund"
   - "What is the exit load?"

3. **Minimum SIP**
   - "Minimum SIP for HDFC Large Cap Fund"
   - "What is the minimum SIP amount?"

4. **Lock-in / ELSS**
   - "ELSS lock-in period?"
   - "What is the lock-in for this fund?"

5. **Riskometer**
   - "Riskometer of SBI Small Cap Fund"
   - "What is the risk rating?"

6. **Benchmark**
   - "Benchmark of Nippon India Growth Fund"
   - "What is the benchmark?"

7. **Statements**
   - "How to download capital gains statement?"
   - "How do I download tax documents?"

### Opinionated Queries (Refused)

- "Should I buy this fund?"
- "Can I invest in this?"
- "Is this a good fund?"
- "Recommend me a fund"

These get a polite refusal with educational link.

## Response Format

```json
{
  "success": true,
  "query": "user query",
  "answer": "Factual answer with information",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "expense_ratio",
  "scheme_name": "Scheme Name (if applicable)"
}
```

## Features

### ✅ Factual Answers
- Extracts scheme names from queries
- Provides accurate factual information
- Includes source URL for verification

### ✅ Citation Links
- Every answer includes one source URL
- Links to official Groww pages
- Educational links for general queries

### ✅ Opinionated Question Handling
- Detects opinionated questions
- Politely refuses with explanation
- Provides educational link

### ✅ Error Handling
- Handles missing scheme names
- Handles missing data gracefully
- Provides helpful error messages

## Data Structure

### Stored Scheme Format

```json
{
  "id": "icici-prudential-banking-psu-debt",
  "scheme_name": "ICICI Prudential Banking & PSU Debt Direct Growth",
  "source_url": "https://groww.in/mutual-funds/...",
  "category": "Debt",
  "facts": {
    "expense_ratio": "1.5%",
    "exit_load": "1% if redeemed within 1 year",
    "minimum_sip": "100",
    "lock_in": "None",
    "riskometer": "Moderate",
    "benchmark": "Nifty Banking & PSU Debt Index"
  }
}
```

## Next Steps

1. **Frontend Integration**: Connect to React/Next.js frontend
2. **Vector Search**: Add semantic search with embeddings
3. **LLM Integration**: Use LLM for better query understanding
4. **Caching**: Add Redis for faster responses
5. **Analytics**: Track query patterns

## Testing

Run test suite:
```bash
python faq_assistant_backend.py
```

This tests:
- Query type detection
- Scheme name extraction
- Factual answer generation
- Opinionated question handling
- Citation links

## Troubleshooting

### No schemes loaded
- Run `python data_storage.py` first
- Check `data/schemes.json` exists

### Scheme not found
- Check scheme name spelling
- Verify scheme exists in database
- Use partial name matching

### API not responding
- Check server is running
- Verify port 5000 is available
- Check logs for errors


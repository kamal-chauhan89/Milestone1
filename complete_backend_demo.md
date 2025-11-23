# Complete Backend Demo - FAQ Assistant

## Overview

This document demonstrates the complete backend system for the Groww Mutual Fund FAQ Assistant, following **Approach 1 (Precompute and Store)**.

## Architecture

```
┌─────────────────┐
│  Data Scraper   │  → Scrapes Groww pages
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Storage   │  → Normalizes & stores data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAQ Backend    │  → Answers queries with citations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Server     │  → REST API endpoint
└─────────────────┘
```

## Setup Steps

### 1. Scrape Data
```bash
python scrape_all_automated.py
```

### 2. Store Data
```bash
python data_storage.py
```

### 3. Test Backend
```bash
python demo_backend.py
```

### 4. Start API Server
```bash
python api_server.py
```

## Supported Query Types

### ✅ Factual Queries

#### 1. Expense Ratio
- "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"
- "What is the expense ratio?"
- "Expense ratio for Axis Floater Fund"

**Response:**
```json
{
  "answer": "The expense ratio of ICICI Prudential Banking & PSU Debt Direct Growth is 1.5%.",
  "source_url": "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth",
  "question_type": "expense_ratio"
}
```

#### 2. Minimum SIP
- "Minimum SIP for HDFC Large Cap Fund"
- "What is the minimum SIP amount?"
- "Min SIP for ICICI Prudential Banking & PSU Debt Fund"

**Response:**
```json
{
  "answer": "For ICICI Prudential Banking & PSU Debt Direct Growth, Minimum SIP: ₹100, First investment: ₹5000, Subsequent investments: ₹1000.",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "minimum_sip"
}
```

#### 3. Exit Load
- "Exit load of SBI Small Cap Fund"
- "What is the exit load?"
- "Exit load for Axis Floater Fund"

**Response:**
```json
{
  "answer": "The exit load for ICICI Prudential Banking & PSU Debt Direct Growth is: 1% if redeemed within 1 year.",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "exit_load"
}
```

#### 4. Lock-in / ELSS
- "ELSS lock-in period?"
- "What is the lock-in period for ELSS funds?"
- "Lock-in period for tax saver funds"

**Response:**
```json
{
  "answer": "The lock-in period for [Scheme Name] is: 3 years (ELSS). ELSS (Equity Linked Savings Scheme) funds have a mandatory 3-year lock-in period as per tax regulations.",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "lock_in"
}
```

#### 5. Riskometer
- "Riskometer of Nippon India Growth Fund"
- "What is the riskometer rating?"
- "Risk rating for ICICI Prudential Banking & PSU Debt Fund"

**Response:**
```json
{
  "answer": "The riskometer rating for ICICI Prudential Banking & PSU Debt Direct Growth is: Moderate.",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "riskometer"
}
```

#### 6. Benchmark
- "Benchmark of HDFC Flexi Cap Fund"
- "What is the benchmark?"
- "Benchmark for Axis Floater Fund"

**Response:**
```json
{
  "answer": "The benchmark for ICICI Prudential Banking & PSU Debt Direct Growth is: Nifty Banking & PSU Debt Index A-II.",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "benchmark"
}
```

#### 7. Statements / Documents
- "How to download capital gains statement?"
- "How do I download tax documents?"
- "Where can I download my mutual fund statements?"

**Response:**
```json
{
  "answer": "To download capital gains statements and tax documents for your mutual fund investments, you can access them through your Groww account. Go to your portfolio, select the fund, and look for the 'Statements' or 'Tax Documents' section.",
  "source_url": "https://groww.in/help/how-to-download-mutual-fund-statements",
  "question_type": "statements"
}
```

#### 8. Additional Queries
- **NAV**: "What is the NAV of [Scheme]?"
- **Fund Manager**: "Who is the fund manager of [Scheme]?"
- **Fund Size**: "What is the fund size of [Scheme]?"

### ❌ Opinionated Queries (Refused)

- "Should I buy ICICI Prudential Banking & PSU Debt Fund?"
- "Is this a good fund to invest in?"
- "Can you recommend a mutual fund?"
- "Should I sell my holdings?"
- "Is it worth investing?"

**Response:**
```json
{
  "answer": "I can only provide factual information about mutual fund schemes, not investment advice. For personalized investment recommendations, please consult with a certified financial advisor. I can help you with factual queries like expense ratios, exit loads, minimum SIP amounts, lock-in periods, riskometer ratings, benchmarks, and how to download statements.",
  "source_url": "https://groww.in/mutual-funds",
  "question_type": "opinionated"
}
```

## Key Features

### ✅ One Citation Per Answer
Every answer includes exactly one source URL:
- For scheme-specific queries: Link to the scheme page
- For general queries: Link to relevant educational page
- For opinionated queries: Link to general mutual funds page

### ✅ Factual Information Only
- No investment advice
- No recommendations
- Only verified facts from Groww website

### ✅ Polite Refusal
- Opinionated questions are refused politely
- Explanation provided
- Educational link included

### ✅ Error Handling
- Missing scheme names handled gracefully
- Missing data handled with helpful messages
- Scheme not found handled with suggestions

## API Usage

### Python
```python
from faq_assistant_backend import FAQAssistant

assistant = FAQAssistant()
result = assistant.answer_query("Expense ratio of ICICI Prudential Banking & PSU Debt Fund")

print(result['answer'])
print(result['source_url'])
```

### REST API
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"}'
```

## Response Format

All responses follow this structure:

```json
{
  "success": true,
  "query": "user query",
  "answer": "Factual answer with information",
  "source_url": "https://groww.in/mutual-funds/...",
  "question_type": "expense_ratio|exit_load|minimum_sip|lock_in|riskometer|benchmark|statements|opinionated",
  "scheme_name": "Scheme Name (if applicable)"
}
```

## Testing

Run the complete demo:
```bash
python demo_backend.py
```

This will test:
- All supported query types
- Opinionated question handling
- Edge cases
- Citation links
- Response formatting

## Next Steps

1. ✅ Backend complete
2. ⏭️ Frontend integration (React/Next.js)
3. ⏭️ Vector search enhancement
4. ⏭️ LLM integration for better understanding


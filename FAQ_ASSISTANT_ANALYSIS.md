# FAQ Assistant: Option Analysis for Groww Mutual Fund Data Collection

## Problem Statement
Build an FAQ assistant that answers facts about Groww mutual fund schemes (expense ratio, exit load, minimum SIP, lock-in, riskometer, benchmark, statements) using only official public pages. Every answer must include one source link. No advice.

## Two Options Comparison

### Option 1: Precompute and Store Data
**Approach**: Scrape/collect data from Groww website once, store it in a database with source URLs, and serve from stored data.

### Option 2: Real-time Scraping with LLM
**Approach**: When a question is asked, use LLM to scrape data from Groww website in real-time and answer the query.

---

## Detailed Comparison

### 1. **Response Time**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Query Response | **Fast** (50-200ms) - Direct database lookup | **Slow** (2-10 seconds) - Scraping + LLM processing |
| User Experience | ✅ Instant answers | ❌ Noticeable delay |
| Scalability | ✅ Handles high traffic easily | ❌ Slower with concurrent requests |

**Winner: Option 1** - Critical for FAQ assistants where users expect instant responses.

---

### 2. **Cost Efficiency**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| LLM API Calls | **Low** - Only for Q&A, not scraping | **High** - Every query triggers LLM scraping |
| Infrastructure | Database storage (cheap) | More compute for real-time scraping |
| Monthly Cost Estimate | $10-50 (storage + occasional updates) | $100-500+ (LLM calls per query) |
| Cost per Query | ~$0.0001 | ~$0.01-0.05 |

**Winner: Option 1** - 10-50x cheaper for high-volume FAQ usage.

---

### 3. **Data Freshness**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Update Frequency | Manual/scheduled (daily/weekly) | Always current |
| Data Staleness Risk | ⚠️ Can be 1-7 days old | ✅ Always fresh |
| Update Complexity | Need to run update script | Automatic |

**Winner: Option 2** - But mutual fund data changes infrequently (monthly/quarterly), so staleness is minimal.

---

### 4. **Reliability & Availability**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Website Down | ✅ Still works (serves cached data) | ❌ Service unavailable |
| Rate Limiting | ✅ No risk (one-time collection) | ❌ High risk of IP blocking |
| Website Structure Changes | ✅ Time to fix before users affected | ❌ Immediate service breakage |
| Error Handling | ✅ Validate data before serving | ❌ Complex error handling needed |

**Winner: Option 1** - Much more reliable for production use.

---

### 5. **Technical Complexity**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Initial Setup | Medium - Need scraper + storage | Low - Just LLM integration |
| Maintenance | Medium - Periodic updates needed | High - Constant monitoring |
| Error Recovery | Easy - Fix scraper, re-run | Hard - Real-time debugging |
| Testing | Easy - Test stored data | Hard - Test live scraping |

**Winner: Option 2** (initially), but Option 1 is better long-term.

---

### 6. **Legal & Ethical Considerations**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Rate Limiting | ✅ Respectful (one-time collection) | ❌ Risk of aggressive scraping |
| Terms of Service | ✅ Less likely to violate | ⚠️ May violate if done frequently |
| Server Load on Groww | ✅ Minimal impact | ❌ Higher impact |

**Winner: Option 1** - More respectful to Groww's servers.

---

### 7. **Data Quality & Validation**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Data Validation | ✅ Can validate before serving | ❌ No pre-validation |
| Quality Control | ✅ Review and fix data issues | ❌ Errors pass to users |
| Source URL Tracking | ✅ Easy to maintain | ⚠️ Complex to track |

**Winner: Option 1** - Better quality control.

---

### 8. **Scalability**

| Aspect | Option 1 (Precompute) | Option 2 (Real-time) |
|--------|----------------------|---------------------|
| Concurrent Users | ✅ Handles thousands easily | ❌ Limited by scraping rate |
| Database Queries | Fast and efficient | N/A |
| Resource Usage | Low and predictable | High and variable |

**Winner: Option 1** - Much better scalability.

---

## Recommendation: **Option 1 (Precompute and Store)**

### Why Option 1 is Better:

1. **Mutual Fund Data Changes Infrequently**
   - Expense ratios, exit loads, minimum SIP amounts change monthly/quarterly at most
   - Daily updates are unnecessary
   - Weekly updates are sufficient

2. **User Experience is Critical**
   - FAQ assistants need instant responses
   - Users expect <1 second response times
   - Real-time scraping adds 2-10 second delays

3. **Cost-Effective at Scale**
   - FAQ assistants typically serve many queries
   - Real-time scraping costs add up quickly
   - Precomputed data is 10-50x cheaper

4. **Production Reliability**
   - FAQ assistants need 99.9% uptime
   - Real-time scraping is fragile (website changes, rate limits, downtime)
   - Precomputed data is resilient

5. **Better Quality Control**
   - Can validate and clean data before serving
   - Can handle edge cases and errors gracefully
   - Users get consistent, reliable answers

---

## Recommended Implementation Strategy (Option 1)

### Architecture:

```
┌─────────────────┐
│  Data Collector │  (Runs daily/weekly)
│  (Scraper)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Database      │  (Stores: scheme_name, expense_ratio, 
│   (JSON/DB)     │   exit_load, min_sip, lock_in, riskometer,
│                 │   benchmark, source_url)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAQ Assistant  │  (Serves queries from database)
│  (LLM + RAG)    │
└─────────────────┘
```

### Implementation Steps:

1. **Data Collection Script** (Python)
   - Scrape Groww mutual fund pages
   - Extract: expense ratio, exit load, min SIP, lock-in, riskometer, benchmark
   - Store with source URL for each scheme
   - Run daily/weekly via cron job

2. **Storage** (Choose one)
   - **JSON files** (simple, good for <1000 schemes)
   - **SQLite** (good for structured queries)
   - **PostgreSQL** (better for complex queries)
   - **Vector DB** (if using RAG for semantic search)

3. **FAQ Assistant** (LLM + RAG)
   - Use RAG (Retrieval Augmented Generation)
   - Query database for relevant scheme data
   - LLM generates answer with source URL
   - Fast response time (<1 second)

4. **Update Mechanism**
   - Scheduled job (daily/weekly)
   - Incremental updates (only changed schemes)
   - Version control for data changes

### Example Data Structure:

```json
{
  "scheme_id": "groww-large-cap-fund",
  "scheme_name": "Groww Large Cap Fund",
  "expense_ratio": "1.5%",
  "exit_load": "1% if redeemed within 1 year",
  "min_sip": "₹500",
  "min_lumpsum": "₹5000",
  "lock_in": "None (except ELSS: 3 years)",
  "riskometer": "Moderately High",
  "benchmark": "Nifty 100",
  "source_url": "https://groww.in/mutual-funds/category/best-large-cap-mutual-funds",
  "last_updated": "2025-01-15"
}
```

---

## Hybrid Approach (Best of Both Worlds)

If you need both freshness and performance:

1. **Primary**: Use Option 1 (precomputed data) for 99% of queries
2. **Fallback**: Use Option 2 (real-time scraping) only when:
   - Data is >7 days old
   - User explicitly requests "latest" data
   - Precomputed data is missing for a scheme

This gives you:
- ✅ Fast responses (Option 1)
- ✅ Fresh data when needed (Option 2)
- ✅ Reliability (Option 1 primary)
- ✅ Cost efficiency (Option 2 only when needed)

---

## Conclusion

**For a production FAQ assistant about Groww mutual funds, Option 1 (Precompute and Store) is the clear winner.**

The data changes infrequently, users expect fast responses, costs are lower, and reliability is better. Implement a scheduled update mechanism (daily/weekly) to keep data fresh, and you'll have the best of both worlds.

**Next Steps:**
1. Build a scraper to collect data from Groww pages
2. Design database schema for storing scheme data
3. Implement scheduled update job
4. Build FAQ assistant with RAG + LLM
5. Add monitoring and alerting for data freshness


# Quick Start Guide - Groww Mutual Fund Scraper

## Installation

```bash
pip install -r requirements.txt
```

## Quick Examples

### 1. Scrape a Single Fund

```python
from groww_scraper import GrowwMutualFundScraper

scraper = GrowwMutualFundScraper()
url = "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth"
data = scraper.scrape_fund_page(url)
print(data)
```

### 2. Scrape All Funds from a Category

```python
from groww_scraper import GrowwMutualFundScraper

scraper = GrowwMutualFundScraper()
category_url = "https://groww.in/mutual-funds/category/best-banking-and-psu-mutual-funds"
funds = scraper.scrape_category(category_url)
scraper.save_data(funds, 'banking_psu_funds.json')
```

### 3. Run Tests

```bash
python test_scraper.py
```

## What Gets Scraped

✅ **Basic Info**: Scheme name, category, NAV, fund size, fund manager  
✅ **Investment Details**: Min SIP, min lumpsum, first/subsequent investment amounts, lock-in  
✅ **Charges**: Expense ratio, exit load  
✅ **Risk**: Riskometer, benchmark  
✅ **Holdings**: Complete holdings list with sectors, instruments, assets  
✅ **Analysis**: Sector allocation, debt/cash breakdown  
✅ **Links**: KIM, SID, factsheet, FAQ, fee pages  
✅ **Source URLs**: Every data point includes source URL for verification

## Output Format

Data is saved as JSON with:
- Pretty formatting
- Source URLs for all data
- Timestamp of scraping
- Validation results

## Example Output

```json
{
  "source_url": "https://groww.in/mutual-funds/...",
  "scheme_name": "ICICI Prudential Banking & PSU Debt",
  "expense_ratio": "1.5%",
  "minimum_investment": {
    "first_investment": "5000",
    "subsequent_investment": "1000",
    "min_sip": "100"
  },
  "sector_allocation": {
    "Financial": "38.3%",
    "Construction": "8.7%"
  },
  "holdings": [...]
}
```

## Next Steps

1. Run `python test_scraper.py` to verify setup
2. Scrape your first fund: `python groww_scraper.py`
3. Check the output JSON file
4. Integrate with your FAQ assistant

## Troubleshooting

**No data extracted?**
- Check internet connection
- Verify URL is accessible
- Run test script first

**Missing fields?**
- Some funds may not have all data
- Check actual Groww page
- Scraper extracts what's available

**Rate limiting?**
- Increase delay in `scrape_category()` method
- Scrape during off-peak hours


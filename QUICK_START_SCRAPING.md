# Quick Start - Complete Scraping

## Your Text File

The script found **373 unique fund URLs** from your text file containing:
- 17 category pages
- 5 AMC pages

## Run Automated Scraping

### Option 1: Automated (Recommended)

This will scrape ALL 373 funds automatically:

```bash
python scrape_all_automated.py
```

**Estimated time:** ~12-15 minutes (2 seconds per fund)

### Option 2: Interactive

Choose what to scrape:

```bash
python scrape_from_txt.py
```

Then select:
- Option 1: Test with 10 funds first
- Option 2: Scrape all 373 funds
- Option 3: Scrape first N funds

### Option 3: Test First

Test with just 10 funds to verify everything works:

```python
from scrape_from_txt import CategoryAMCScraper
from batch_scraper import BatchMutualFundScraper

# Extract URLs
category_scraper = CategoryAMCScraper()
links_data = category_scraper.load_links_from_txt(
    r"C:\Users\sweet\projects\Groww links for mutual funds.txt"
)
all_fund_urls = category_scraper.extract_all_fund_urls(links_data)

# Test with 10 funds
batch_scraper = BatchMutualFundScraper()
batch_scraper.scrape_urls(all_fund_urls, max_urls=10)
batch_scraper.save_progress('test_scraped.json')
```

## Output Files

After scraping, you'll get:

1. **`all_extracted_fund_urls.json`**
   - All 373 fund URLs extracted
   - Use this to resume scraping if interrupted

2. **`groww_all_funds_scraped.json`**
   - Complete scraped data for all funds
   - Includes:
     - Scheme name, NAV, expense ratio
     - Minimum SIP, exit load, lock-in
     - Holdings, sector allocation
     - Riskometer, benchmark
     - Source URLs for all data

## Resume Scraping

If scraping is interrupted, you can resume:

```python
from batch_scraper import BatchMutualFundScraper
import json

# Load extracted URLs
with open('all_extracted_fund_urls.json', 'r') as f:
    data = json.load(f)
    fund_urls = data['fund_urls']

# Resume from URL 100 (if you stopped there)
batch_scraper = BatchMutualFundScraper()
batch_scraper.scrape_urls(fund_urls, start_index=100)
```

## What Gets Scraped

For each of the 373 funds:

✅ **Basic Info**: Scheme name, category, NAV, fund size, fund manager  
✅ **Investment**: Min SIP, min lumpsum, first/subsequent investment, lock-in  
✅ **Charges**: Expense ratio, exit load  
✅ **Risk**: Riskometer, benchmark  
✅ **Holdings**: Complete list with sectors, instruments, assets %  
✅ **Analysis**: Sector allocation, debt/cash breakdown  
✅ **Links**: KIM, SID, factsheet, FAQ, fee pages  
✅ **Source URLs**: Every data point includes source URL

## Progress Monitoring

The scraper shows real-time progress:
```
[1/373] Processing: https://groww.in/mutual-funds/...
  [OK] Success: ICICI Prudential Banking & PSU Debt
[2/373] Processing: https://groww.in/mutual-funds/...
  [OK] Success: Axis Floater Fund
...
```

## Tips

1. **Start with test**: Run with 10 funds first to verify
2. **Let it run**: Full scraping takes ~12-15 minutes
3. **Check output**: Review `groww_all_funds_scraped.json` after completion
4. **Resume if needed**: Use `start_index` to resume from where you left off

## Next Steps

After scraping:
1. Review the JSON output file
2. Validate data quality
3. Import into your FAQ assistant database
4. Use for your RAG system


# Testing Guide for Groww Mutual Fund Scraper

## Step-by-Step Testing Process

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have:
- beautifulsoup4
- requests
- lxml
- python-docx (for .docx file parsing)

### Step 2: Verify Document Path

Make sure your document is at:
```
D:\download\Groww links for mutual funds.docx
```

Or update the path in the scripts.

### Step 3: Run Test Suite

```bash
python test_batch_scraper.py
```

This will test:
1. ✅ Document parsing (can we read your .docx file?)
2. ✅ URL validation (are the URLs valid?)
3. ✅ Single fund scraping (can we scrape one fund?)
4. ✅ Batch scraping (can we scrape multiple funds?)

### Step 4: Check Test Results

After running tests, you should see:
- `test_extracted_links.json` - All extracted links from your document
- `test_scraped_data.json` - Sample scraped data (if batch test passed)

### Step 5: Review Extracted Links

Open `test_extracted_links.json` to see:
- Total number of schemes found
- How they're organized by AMC
- Sample URLs

### Step 6: Start Full Scraping

Once tests pass, run the full scraper:

```bash
python run_batch_scrape.py
```

Or use Python:

```python
from batch_scraper import BatchMutualFundScraper

batch_scraper = BatchMutualFundScraper()
links_data = batch_scraper.load_links_from_document(
    r"D:\download\Groww links for mutual funds.docx"
)

# Start with small test
batch_scraper.scrape_urls(links_data['all_schemes'], max_urls=10)

# Then full scrape
batch_scraper.scrape_urls(links_data['all_schemes'])
```

## Troubleshooting

### Test 1 Fails: Document Parsing

**Error: File not found**
- Check file path is correct
- File should be `.docx` format

**Error: Missing python-docx**
```bash
pip install python-docx
```

**No URLs extracted**
- Check document actually contains Groww URLs
- URLs should be in format: `https://groww.in/mutual-funds/...`

### Test 2 Fails: URL Validation

- Check if URLs in document are valid Groww URLs
- URLs should start with `https://groww.in/mutual-funds/`

### Test 3 Fails: Single Fund Scraping

**Network Error**
- Check internet connection
- Verify Groww website is accessible
- Try accessing the URL in browser

**No Data Extracted**
- Website structure might have changed
- Check if the fund page is accessible
- Review the scraper extraction methods

### Test 4 Fails: Batch Scraping

- Usually means single fund scraping failed
- Fix Test 3 first
- Check rate limiting (increase delay)

## Expected Results

### Successful Test Output

```
✅ Document parsed successfully!
   Total URLs found: 500
   AMCs found: 25

✅ All URL validations passed!

✅ Successfully scraped fund data!
   Scheme Name: ICICI Prudential Banking & PSU Debt
   NAV: 35.07
   Expense Ratio: 1.5%
   Min SIP: 100

✅ Batch scraping test complete!
   Successful: 3
   Failed: 0
```

### Output Files

1. **test_extracted_links.json**
   - All URLs from your document
   - Organized by AMC (if detected)

2. **test_scraped_data.json**
   - Sample scraped fund data
   - Includes metadata and statistics

3. **groww_scraped_all_[timestamp].json** (after full scrape)
   - Complete scraped data
   - All schemes with full details

## Next Steps After Testing

1. ✅ All tests pass → Ready for full scraping
2. Review extracted links count
3. Estimate scraping time (2 seconds per fund)
4. Start full scraping during off-peak hours
5. Monitor progress and check output files

## Performance Estimates

- **Small test (10 funds)**: ~20 seconds
- **Medium (100 funds)**: ~3-4 minutes
- **Large (500 funds)**: ~15-20 minutes
- **Full (1000+ funds)**: ~30-60 minutes

Adjust delay between requests if needed (default: 2 seconds).


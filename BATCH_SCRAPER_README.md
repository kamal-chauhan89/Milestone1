# Batch Scraper for Groww Mutual Funds

Complete solution for scraping all AMCs and schemes from a document containing Groww mutual fund links.

## Features

- ✅ Parse links from .docx, .txt, and .csv files
- ✅ Organize links by AMC (Asset Management Company)
- ✅ Batch scraping with progress tracking
- ✅ Automatic progress saving
- ✅ Error handling and retry logic
- ✅ Statistics and summary reports

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Step 1: Extract Links from Document

```python
from document_link_parser import DocumentLinkParser

parser = DocumentLinkParser()
doc_path = r"D:\download\Groww links for mutual funds.docx"

# Extract links
links_data = parser.parse_document(doc_path)

# Save extracted links
parser.save_extracted_links(links_data, 'groww_all_scheme_links.json')

print(f"Total schemes: {len(links_data['all_schemes'])}")
print(f"AMCs found: {len(links_data['organized_by_amc'])}")
```

### Step 2: Run Batch Scraping

```python
from batch_scraper import BatchMutualFundScraper

batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)

# Load links from document
links_data = batch_scraper.load_links_from_document(
    r"D:\download\Groww links for mutual funds.docx"
)

# Scrape all schemes
batch_scraper.scrape_urls(links_data['all_schemes'])

# Save results
batch_scraper.save_progress()
batch_scraper.print_summary()
```

### Step 3: Run from Command Line

```bash
python batch_scraper.py
```

## Usage Options

### Option 1: Scrape All Schemes

Scrapes all schemes from the document in sequence.

```python
batch_scraper.scrape_urls(links_data['all_schemes'])
```

### Option 2: Scrape by AMC

Scrapes schemes organized by AMC, saves progress after each AMC.

```python
batch_scraper.scrape_by_amc(links_data)
```

### Option 3: Scrape Specific AMC

Scrape schemes for a specific AMC only.

```python
batch_scraper.scrape_by_amc(links_data, amc_name="ICICI Prudential Mutual Fund")
```

### Option 4: Test with Limited Schemes

Test the scraper with first N schemes.

```python
batch_scraper.scrape_urls(links_data['all_schemes'], max_urls=10)
```

## Document Format Support

### .docx Files
- Extracts URLs from paragraph text
- Extracts hyperlinks
- Attempts to organize by AMC based on headings

### .txt Files
- Extracts URLs using regex
- Organizes by AMC if patterns are detected

### .csv Files
- Supports CSV with AMC and URL columns
- Automatically detects column headers

## Output Format

### Extracted Links JSON
```json
{
  "all_schemes": [
    "https://groww.in/mutual-funds/...",
    ...
  ],
  "organized_by_amc": {
    "ICICI Prudential Mutual Fund": [
      "https://groww.in/mutual-funds/...",
      ...
    ],
    ...
  }
}
```

### Scraped Data JSON
```json
{
  "metadata": {
    "scraped_at": "2025-01-15T10:30:00",
    "total_schemes": 150,
    "stats": {
      "total_urls": 150,
      "successful": 145,
      "failed": 3,
      "skipped": 2
    }
  },
  "schemes": [
    {
      "source_url": "https://groww.in/mutual-funds/...",
      "scheme_name": "...",
      ...
    }
  ],
  "failed_urls": [
    {
      "url": "...",
      "reason": "...",
      "timestamp": "..."
    }
  ]
}
```

## Configuration

### Adjust Delay Between Requests

```python
# Faster (1 second delay)
batch_scraper = BatchMutualFundScraper(delay_between_requests=1.0)

# Slower (3 seconds delay - more respectful)
batch_scraper = BatchMutualFundScraper(delay_between_requests=3.0)
```

### Resume from Specific Index

```python
# Resume from URL index 100
batch_scraper.scrape_urls(
    links_data['all_schemes'],
    start_index=100
)
```

## Progress Tracking

The batch scraper automatically:
- Saves progress after each AMC (when scraping by AMC)
- Tracks successful, failed, and skipped URLs
- Provides real-time progress updates
- Saves final summary with statistics

## Error Handling

- Invalid URLs are skipped
- Failed scrapes are logged with reasons
- Network errors are caught and logged
- Progress is saved even if scraping is interrupted

## Statistics

After scraping, you get:
- Total URLs processed
- Successful scrapes count
- Failed scrapes count
- Skipped URLs (insufficient data)
- Success rate percentage

## Example Workflow

```python
from batch_scraper import BatchMutualFundScraper

# Initialize
batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)

# Load document
doc_path = r"D:\download\Groww links for mutual funds.docx"
links_data = batch_scraper.load_links_from_document(doc_path)

# Check what we have
print(f"Total schemes: {len(links_data['all_schemes'])}")
if links_data['organized_by_amc']:
    print(f"AMCs: {len(links_data['organized_by_amc'])}")
    for amc, schemes in links_data['organized_by_amc'].items():
        print(f"  {amc}: {len(schemes)} schemes")

# Scrape all (or use scrape_by_amc for organized scraping)
batch_scraper.scrape_urls(links_data['all_schemes'])

# Save results
batch_scraper.save_progress('all_groww_funds.json')
batch_scraper.print_summary()
```

## Tips

1. **Start Small**: Test with 5-10 schemes first
2. **Monitor Progress**: Check the console output regularly
3. **Save Frequently**: Progress is auto-saved when scraping by AMC
4. **Resume Capability**: Use `start_index` to resume from where you left off
5. **Respect Rate Limits**: Keep delay at 2+ seconds to avoid blocking

## Troubleshooting

### Document Not Parsing
- Check file path is correct
- Verify file format is supported (.docx, .txt, .csv)
- Install python-docx: `pip install python-docx`

### No Links Extracted
- Check document actually contains Groww URLs
- Verify URLs are in format: `https://groww.in/mutual-funds/...`
- Try extracting from text manually to verify

### Scraping Fails
- Check internet connection
- Verify Groww website is accessible
- Increase delay between requests
- Check if URLs are still valid

### Memory Issues
- Process in batches (use `max_urls` parameter)
- Save progress frequently
- Scrape by AMC instead of all at once

## Next Steps

After scraping:
1. Review the scraped data JSON file
2. Validate data quality
3. Import into your FAQ assistant database
4. Set up scheduled updates


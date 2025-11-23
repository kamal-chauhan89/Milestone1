# Groww Mutual Fund Scraper

A comprehensive web scraper for extracting mutual fund data from Groww website, including expense ratios, exit loads, minimum SIP amounts, holdings, sector allocations, and more.

## Features

- ✅ Extracts all key mutual fund data points
- ✅ Validates URLs and data integrity
- ✅ Stores data with source URLs
- ✅ Handles category pages to scrape multiple funds
- ✅ Extracts holdings and sector allocations
- ✅ Debt and cash analysis
- ✅ Return calculator detection
- ✅ Links to KIM, SID, factsheets

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage - Scrape Single Fund

```python
from groww_scraper import GrowwMutualFundScraper

scraper = GrowwMutualFundScraper()
fund_url = "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth"
fund_data = scraper.scrape_fund_page(fund_url)

print(fund_data)
```

### Scrape Category Page

```python
from groww_scraper import GrowwMutualFundScraper

scraper = GrowwMutualFundScraper()
category_url = "https://groww.in/mutual-funds/category/best-banking-and-psu-mutual-funds"
all_funds = scraper.scrape_category(category_url)

# Save to JSON
scraper.save_data(all_funds, 'groww_funds.json')
```

### Run from Command Line

```bash
python groww_scraper.py
```

## Data Structure

Each scraped fund contains:

```json
{
  "source_url": "https://groww.in/mutual-funds/...",
  "scraped_at": "2025-01-15T10:30:00",
  "scheme_name": "ICICI Prudential Banking & PSU Debt Direct Growth",
  "category": "Debt",
  "nav": "35.07",
  "expense_ratio": "1.5%",
  "exit_load": "1% if redeemed within 1 year",
  "minimum_investment": {
    "first_investment": "5000",
    "subsequent_investment": "1000",
    "min_sip": "100",
    "min_lumpsum": "500"
  },
  "lock_in": "None",
  "riskometer": "Moderate",
  "benchmark": "Nifty Banking & PSU Debt Index A-II",
  "fund_size": "₹9,764.38Cr",
  "fund_manager": "Rohit Lakhotia",
  "holdings": [
    {
      "name": "LIC Housing Finance Ltd.",
      "sector": "Financial",
      "instrument": "NCD",
      "assets": "4.70%"
    }
  ],
  "sector_allocation": {
    "Financial": "38.3%",
    "Construction": "8.7%"
  },
  "debt_cash_analysis": {
    "total_debt": "85.5%",
    "total_cash": "5.2%",
    "debt_breakdown": {},
    "cash_breakdown": {}
  },
  "return_calculator": {
    "has_calculator": true,
    "calculator_url": "..."
  },
  "additional_links": {
    "kim_url": "...",
    "sid_url": "...",
    "factsheet_url": "...",
    "faq_url": "...",
    "fee_charges_url": "..."
  }
}
```

## Extracted Data Points

### Core Information
- Scheme name
- Category (Equity/Debt/Hybrid)
- NAV (Net Asset Value)
- Fund size (AUM)
- Fund manager

### Investment Details
- Minimum SIP amount
- Minimum lumpsum amount
- First investment minimum
- Subsequent investment minimum
- Lock-in period (for ELSS)

### Charges & Risk
- Expense ratio
- Exit load
- Riskometer rating
- Benchmark

### Holdings & Analysis
- Complete holdings list
- Sector allocation percentages
- Debt holdings breakdown
- Cash holdings breakdown
- Instrument types

### Additional Resources
- Return calculator availability
- Links to KIM (Key Information Memorandum)
- Links to SID (Scheme Information Document)
- Factsheet links
- FAQ links
- Fee/charges page links

## URL Validation

The scraper validates all URLs to ensure:
- URL belongs to groww.in domain
- URL is a valid mutual fund page
- No invalid or broken URLs are stored

## Data Validation

Each scraped fund is validated for:
- Presence of source URL
- Presence of scheme name
- URL validity
- Minimum required data

## Example Categories to Scrape

- Large Cap: `https://groww.in/mutual-funds/category/best-large-cap-mutual-funds`
- Banking & PSU: `https://groww.in/mutual-funds/category/best-banking-and-psu-mutual-funds`
- Mid Cap: `https://groww.in/mutual-funds/category/best-mid-cap-mutual-funds`
- Small Cap: `https://groww.in/mutual-funds/category/best-small-cap-mutual-funds`
- ELSS: `https://groww.in/mutual-funds/category/best-elss-mutual-funds`

## Rate Limiting

The scraper includes a 2-second delay between requests to be respectful to Groww's servers. Adjust in the `scrape_category` method if needed.

## Error Handling

- Invalid URLs are skipped with warnings
- Failed page fetches are logged
- Missing data fields are set to `None`
- Validation results are included in output

## Output Files

Data is saved as JSON files with:
- Pretty formatting (indented)
- UTF-8 encoding
- All source URLs preserved
- Timestamp of scraping

## Notes

- The scraper uses BeautifulSoup for HTML parsing
- No JavaScript rendering is required (static HTML)
- All data is extracted from public pages only
- Source URLs are always included for verification

## Troubleshooting

### No data extracted
- Check if the URL is accessible
- Verify the page structure hasn't changed
- Check network connectivity

### Missing fields
- Some funds may not have all data points
- Check the actual Groww page to verify
- The scraper will extract what's available

### Rate limiting
- Increase delay between requests
- Use proxy rotation if needed
- Scrape during off-peak hours

## Legal & Ethical Considerations

- Only scrapes public pages
- Respects rate limits
- Includes source attribution
- No personal data collection
- For informational purposes only

## Future Enhancements

- [ ] Add Selenium support for JavaScript-rendered content
- [ ] Add database storage option (PostgreSQL, MongoDB)
- [ ] Add incremental update capability
- [ ] Add data change detection
- [ ] Add email alerts for data updates
- [ ] Add API endpoint for querying scraped data


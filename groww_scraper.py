"""
Groww Mutual Fund Data Scraper
Scrapes mutual fund data from Groww website and stores with source URLs
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import time
from datetime import datetime


class GrowwMutualFundScraper:
    def __init__(self):
        self.base_url = "https://groww.in"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.scraped_data = []

    def validate_url(self, url: str) -> bool:
        """Validate that URL is a valid Groww mutual fund URL"""
        if not url or not isinstance(url, str):
            return False
        
        parsed = urlparse(url)
        if parsed.netloc not in ['groww.in', 'www.groww.in']:
            return False
        
        # Check if it's a mutual fund URL
        if '/mutual-funds/' not in url:
            return False
        
        return True

    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        if not self.validate_url(url):
            print(f"Invalid URL: {url}")
            return None
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_text_content(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Try multiple selectors to extract text"""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return None

    def extract_nav(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract NAV (Net Asset Value)"""
        # Look for NAV in specific patterns - usually shown as "NAV: 21 Nov 2025 ₹35.07"
        nav_patterns = [
            re.compile(r'NAV[:\s]*\d+\s*\w+\s*\d+[:\s]*₹?\s*([\d,]+\.?\d*)', re.IGNORECASE),
            re.compile(r'NAV[:\s]*₹?\s*([\d,]+\.?\d*)', re.IGNORECASE),
            re.compile(r'₹\s*([\d,]+\.?\d*)\s*NAV', re.IGNORECASE),
        ]
        
        text = soup.get_text()
        for pattern in nav_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).replace(',', '')
        
        # Try finding in structured elements
        nav_elements = soup.find_all(string=re.compile(r'NAV', re.IGNORECASE))
        for element in nav_elements:
            parent = element.find_parent()
            if parent:
                text_content = parent.get_text()
                nav_match = re.search(r'₹?\s*([\d,]+\.?\d*)', text_content)
                if nav_match:
                    return nav_match.group(1).replace(',', '')
        
        return None

    def extract_expense_ratio(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract expense ratio"""
        expense_ratio = self.extract_text_content(soup, [
            '[class*="expense"]',
            'div:contains("Expense Ratio")',
        ])
        
        # Pattern matching for expense ratio
        expense_pattern = re.compile(r'expense\s*ratio[:\s]*([\d.]+%)', re.IGNORECASE)
        text = soup.get_text()
        match = expense_pattern.search(text)
        if match:
            return match.group(1)
        
        return expense_ratio

    def extract_exit_load(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract exit load information"""
        exit_load = self.extract_text_content(soup, [
            '[class*="exit"]',
            'div:contains("Exit Load")',
        ])
        
        # Pattern matching
        exit_pattern = re.compile(r'exit\s*load[:\s]*([^\.]+)', re.IGNORECASE)
        text = soup.get_text()
        match = exit_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        return exit_load

    def extract_minimum_investment(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract minimum investment amounts"""
        min_investment = {
            'first_investment': None,
            'subsequent_investment': None,
            'min_sip': None,
            'min_lumpsum': None,
        }
        
        text = soup.get_text()
        
        # Pattern for minimum SIP - look for "Min. SIP amount" followed by ₹
        sip_patterns = [
            re.compile(r'Min[.\s]*SIP[:\s]*amount[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'SIP[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
        ]
        for pattern in sip_patterns:
            match = pattern.search(text)
            if match:
                min_investment['min_sip'] = match.group(1).replace(',', '')
                break
        
        # Pattern for minimum lumpsum
        lumpsum_patterns = [
            re.compile(r'Min[.\s]*Lumpsum[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'Lumpsum[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
        ]
        for pattern in lumpsum_patterns:
            match = pattern.search(text)
            if match:
                min_investment['min_lumpsum'] = match.group(1).replace(',', '')
                break
        
        # Look for "1st investment" and "2nd investment onwards" patterns
        # Example: "Minimum investment amount for 1st investment is 5000 rupees and for 2nd investment onwards it is 1000 rupees"
        first_patterns = [
            re.compile(r'1st\s*investment[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'first\s*investment[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'minimum[^.]*1st[^.]*₹?\s*([\d,]+)', re.IGNORECASE),
        ]
        for pattern in first_patterns:
            match = pattern.search(text)
            if match:
                min_investment['first_investment'] = match.group(1).replace(',', '')
                break
        
        second_patterns = [
            re.compile(r'2nd\s*investment[:\s]*onwards[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'2nd\s*investment[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'second\s*investment[:\s]*onwards[:\s]*₹?\s*([\d,]+)', re.IGNORECASE),
            re.compile(r'subsequent[^.]*₹?\s*([\d,]+)', re.IGNORECASE),
        ]
        for pattern in second_patterns:
            match = pattern.search(text)
            if match:
                min_investment['subsequent_investment'] = match.group(1).replace(',', '')
                break
        
        # Also check for structured data in divs/spans
        sip_elements = soup.find_all(string=re.compile(r'Min[.\s]*SIP', re.IGNORECASE))
        for element in sip_elements:
            parent = element.find_parent()
            if parent:
                text_content = parent.get_text()
                numbers = re.findall(r'₹?\s*([\d,]+)', text_content)
                if numbers:
                    min_investment['min_sip'] = numbers[0].replace(',', '')
                    break
        
        return min_investment

    def extract_lock_in(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lock-in period (especially for ELSS)"""
        text = soup.get_text()
        
        # Pattern for lock-in
        lockin_pattern = re.compile(r'lock[-\s]*in[:\s]*([^\.]+)', re.IGNORECASE)
        match = lockin_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        # Check for ELSS (3 years lock-in)
        if 'ELSS' in text.upper() or 'tax saver' in text.lower():
            return "3 years (ELSS)"
        
        return None

    def extract_riskometer(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract riskometer rating"""
        riskometer = self.extract_text_content(soup, [
            '[class*="risk"]',
            'div:contains("Risk")',
        ])
        
        # Pattern matching
        risk_pattern = re.compile(r'risk[ometer]*[:\s]*([^\.]+)', re.IGNORECASE)
        text = soup.get_text()
        match = risk_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        # Look for risk levels
        risk_levels = ['Low', 'Moderate', 'Moderately High', 'High', 'Very High']
        for level in risk_levels:
            if level in text:
                return level
        
        return riskometer

    def extract_benchmark(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract benchmark information"""
        benchmark = self.extract_text_content(soup, [
            '[class*="benchmark"]',
            'div:contains("Benchmark")',
        ])
        
        # Pattern matching
        benchmark_pattern = re.compile(r'benchmark[:\s]*([^\.]+)', re.IGNORECASE)
        text = soup.get_text()
        match = benchmark_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        # Look for "Fund benchmark" section
        benchmark_section = soup.find(string=re.compile(r'Fund\s*benchmark', re.IGNORECASE))
        if benchmark_section:
            parent = benchmark_section.find_parent()
            if parent:
                next_sibling = parent.find_next_sibling()
                if next_sibling:
                    return next_sibling.get_text(strip=True)
        
        return benchmark

    def extract_holdings(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract holdings information"""
        holdings = []
        holdings_table = None
        
        # Look for holdings table - check for "Holdings" heading
        holdings_section = soup.find(string=re.compile(r'Holdings', re.IGNORECASE))
        if holdings_section:
            # Find the table near the holdings heading
            parent = holdings_section.find_parent()
            if parent:
                holdings_table = parent.find_next('table')
                if not holdings_table:
                    # Try finding table in nearby siblings
                    for sibling in parent.find_next_siblings():
                        holdings_table = sibling.find('table')
                        if holdings_table:
                            break
        
        # If not found, try finding any table
        if not holdings_table:
            tables = soup.find_all('table')
            # Prefer tables with more columns (likely holdings table)
            if tables:
                holdings_table = max(tables, key=lambda t: len(t.find_all('th')))
        
        if holdings_table:
            headers = []
            header_row = holdings_table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            elif holdings_table.find('tr'):
                # Headers might be in first row
                first_row = holdings_table.find('tr')
                headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
            
            rows = holdings_table.find('tbody')
            if not rows:
                rows = holdings_table
            
            if rows:
                for row in rows.find_all('tr'):
                    # Skip header row
                    if row.find('th'):
                        continue
                    
                    cells = [td.get_text(strip=True) for td in row.find_all('td')]
                    if cells and len(cells) >= 2:
                        holding = {}
                        for i, header in enumerate(headers):
                            if i < len(cells):
                                key = header.lower().replace(' ', '_').replace('.', '')
                                holding[key] = cells[i]
                        if holding:
                            holdings.append(holding)
        
        return holdings

    def extract_sector_allocation(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract sector allocation percentages"""
        sector_allocation = {}
        
        # Look for sector allocation in holdings table
        # Check for table with "Sector" column
        tables = soup.find_all('table')
        for table in tables:
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text(strip=True).lower() for th in header_row.find_all('th')]
            
            if 'sector' in headers:
                sector_col_idx = headers.index('sector')
                assets_col_idx = headers.index('assets') if 'assets' in headers else None
                
                rows = table.find('tbody')
                if rows:
                    for row in rows.find_all('tr'):
                        cells = [td.get_text(strip=True) for td in row.find_all('td')]
                        if len(cells) > sector_col_idx:
                            sector = cells[sector_col_idx]
                            if assets_col_idx and len(cells) > assets_col_idx:
                                percentage = cells[assets_col_idx]
                                if percentage and '%' in percentage:
                                    sector_allocation[sector] = percentage
        
        # Also look for sector allocation in text patterns
        text = soup.get_text()
        
        # Pattern: "Financial sector debt: 38.3%" or "Financial: 38.3%"
        sector_patterns = [
            re.compile(r'([A-Za-z\s]+)\s*(?:sector|allocation)[:\s]*([\d.]+%)', re.IGNORECASE),
            re.compile(r'([A-Za-z\s]+)[:\s]*([\d.]+%)', re.IGNORECASE),
        ]
        
        # Common sectors to look for
        common_sectors = [
            'Financial', 'Construction', 'Energy', 'Communication', 'Sovereign',
            'Others', 'Debt', 'Cash', 'Equity', 'Government', 'Banking', 'PSU'
        ]
        
        for sector in common_sectors:
            pattern = re.compile(rf'{re.escape(sector)}[:\s]*([\d.]+%)', re.IGNORECASE)
            match = pattern.search(text)
            if match and sector not in sector_allocation:
                sector_allocation[sector] = match.group(1)
        
        return sector_allocation

    def extract_fund_manager(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract fund manager name"""
        manager = self.extract_text_content(soup, [
            '[class*="manager"]',
            'div:contains("Fund Manager")',
        ])
        
        # Pattern matching
        manager_pattern = re.compile(r'fund\s*manager[:\s]*([^\.]+)', re.IGNORECASE)
        text = soup.get_text()
        match = manager_pattern.search(text)
        if match:
            return match.group(1).strip()
        
        return manager

    def extract_fund_size(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract fund size (AUM)"""
        fund_size = self.extract_text_content(soup, [
            '[class*="fund.*size"]',
            '[class*="aum"]',
        ])
        
        # Pattern matching
        size_pattern = re.compile(r'fund\s*size[:\s]*₹?\s*([\d,]+\.?\d*[CrL]+)', re.IGNORECASE)
        text = soup.get_text()
        match = size_pattern.search(text)
        if match:
            return match.group(1)
        
        return fund_size

    def extract_scheme_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract scheme name"""
        # Usually in h1 or title
        name = self.extract_text_content(soup, [
            'h1',
            'title',
            '[class*="scheme.*name"]',
        ])
        return name

    def extract_category(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract fund category"""
        category = self.extract_text_content(soup, [
            '[class*="category"]',
        ])
        
        # Look for category in text
        text = soup.get_text()
        category_keywords = ['Equity', 'Debt', 'Hybrid', 'Large Cap', 'Mid Cap', 'Small Cap', 'ELSS']
        for keyword in category_keywords:
            if keyword in text:
                return keyword
        
        return category

    def extract_return_calculator_info(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract return calculator information"""
        calculator_info = {
            'has_calculator': False,
            'calculator_url': None,
        }
        
        # Look for return calculator link
        calculator_link = soup.find('a', href=re.compile(r'calculator', re.IGNORECASE))
        if calculator_link:
            calculator_info['has_calculator'] = True
            href = calculator_link.get('href')
            if href:
                calculator_info['calculator_url'] = urljoin(self.base_url, href)
        
        # Also check for "Return calculator" text
        if 'return calculator' in soup.get_text().lower():
            calculator_info['has_calculator'] = True
        
        return calculator_info

    def extract_debt_cash_analysis(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract debt and cash holdings analysis"""
        analysis = {
            'total_debt': None,
            'total_cash': None,
            'debt_breakdown': {},
            'cash_breakdown': {},
        }
        
        text = soup.get_text()
        holdings = self.extract_holdings(soup)
        
        # Calculate debt and cash from holdings
        total_debt = 0.0
        total_cash = 0.0
        
        for holding in holdings:
            # Check if it's debt instrument
            instrument = holding.get('instrument', '').lower()
            assets_str = holding.get('assets', '').replace('%', '').strip()
            
            try:
                assets = float(assets_str)
                if 'debt' in instrument or 'bond' in instrument or 'ncd' in instrument or 'debenture' in instrument:
                    total_debt += assets
                    analysis['debt_breakdown'][holding.get('name', 'Unknown')] = assets_str + '%'
                elif 'cash' in instrument.lower() or 'deposit' in instrument.lower():
                    total_cash += assets
                    analysis['cash_breakdown'][holding.get('name', 'Unknown')] = assets_str + '%'
            except (ValueError, TypeError):
                pass
        
        if total_debt > 0:
            analysis['total_debt'] = f"{total_debt:.2f}%"
        if total_cash > 0:
            analysis['total_cash'] = f"{total_cash:.2f}%"
        
        # Also look for explicit mentions in text
        debt_pattern = re.compile(r'total\s*debt[:\s]*([\d.]+%)', re.IGNORECASE)
        match = debt_pattern.search(text)
        if match:
            analysis['total_debt'] = match.group(1)
        
        cash_pattern = re.compile(r'total\s*cash[:\s]*([\d.]+%)', re.IGNORECASE)
        match = cash_pattern.search(text)
        if match:
            analysis['total_cash'] = match.group(1)
        
        return analysis

    def extract_additional_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Optional[str]]:
        """Extract links to KIM, SID, factsheets, etc."""
        links = {
            'kim_url': None,
            'sid_url': None,
            'factsheet_url': None,
            'faq_url': None,
            'fee_charges_url': None,
        }
        
        # Look for SID link
        sid_link = soup.find('a', href=re.compile(r'sid|scheme.*information', re.IGNORECASE))
        if sid_link:
            links['sid_url'] = urljoin(base_url, sid_link.get('href'))
        
        # Look for KIM link
        kim_link = soup.find('a', href=re.compile(r'kim|key.*information', re.IGNORECASE))
        if kim_link:
            links['kim_url'] = urljoin(base_url, kim_link.get('href'))
        
        # Look for factsheet
        factsheet_link = soup.find('a', href=re.compile(r'factsheet', re.IGNORECASE))
        if factsheet_link:
            links['factsheet_url'] = urljoin(base_url, factsheet_link.get('href'))
        
        return links

    def scrape_fund_page(self, url: str) -> Optional[Dict]:
        """Scrape all data from a single mutual fund page"""
        if not self.validate_url(url):
            print(f"Invalid URL: {url}")
            return None
        
        print(f"Scraping: {url}")
        soup = self.get_page(url)
        if not soup:
            return None
        
        fund_data = {
            'source_url': url,
            'scraped_at': datetime.now().isoformat(),
            'scheme_name': self.extract_scheme_name(soup),
            'category': self.extract_category(soup),
            'nav': self.extract_nav(soup),
            'expense_ratio': self.extract_expense_ratio(soup),
            'exit_load': self.extract_exit_load(soup),
            'minimum_investment': self.extract_minimum_investment(soup),
            'lock_in': self.extract_lock_in(soup),
            'riskometer': self.extract_riskometer(soup),
            'benchmark': self.extract_benchmark(soup),
            'fund_size': self.extract_fund_size(soup),
            'fund_manager': self.extract_fund_manager(soup),
            'holdings': self.extract_holdings(soup),
            'sector_allocation': self.extract_sector_allocation(soup),
            'debt_cash_analysis': self.extract_debt_cash_analysis(soup),
            'return_calculator': self.extract_return_calculator_info(soup),
            'additional_links': self.extract_additional_links(soup, url),
        }
        
        # Validate that we got at least some data
        if not fund_data['scheme_name']:
            print(f"Warning: Could not extract scheme name from {url}")
        
        return fund_data

    def get_fund_urls_from_category(self, category_url: str) -> List[str]:
        """Get all fund URLs from a category page"""
        if not self.validate_url(category_url):
            print(f"Invalid category URL: {category_url}")
            return []
        
        print(f"Fetching fund URLs from category: {category_url}")
        soup = self.get_page(category_url)
        if not soup:
            return []
        
        fund_urls = []
        
        # Find all links to mutual fund pages
        # Groww typically uses links like /mutual-funds/fund-name
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and '/mutual-funds/' in href:
                # Skip category pages
                if '/category/' not in href and '/mutual-funds/' in href:
                    full_url = urljoin(self.base_url, href)
                    if self.validate_url(full_url) and full_url not in fund_urls:
                        fund_urls.append(full_url)
        
        print(f"Found {len(fund_urls)} fund URLs")
        return fund_urls

    def scrape_category(self, category_url: str) -> List[Dict]:
        """Scrape all funds from a category page"""
        fund_urls = self.get_fund_urls_from_category(category_url)
        all_fund_data = []
        
        for i, url in enumerate(fund_urls, 1):
            print(f"\nProcessing fund {i}/{len(fund_urls)}")
            fund_data = self.scrape_fund_page(url)
            if fund_data:
                all_fund_data.append(fund_data)
                # Be respectful - add delay between requests
                time.sleep(2)
        
        return all_fund_data

    def save_data(self, data: List[Dict], filename: str = 'groww_fund_data.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nData saved to {filename}")

    def validate_data(self, fund_data: Dict) -> Dict[str, bool]:
        """Validate scraped data"""
        validation = {
            'has_source_url': bool(fund_data.get('source_url')),
            'has_scheme_name': bool(fund_data.get('scheme_name')),
            'url_is_valid': self.validate_url(fund_data.get('source_url', '')),
            'has_minimum_data': bool(fund_data.get('scheme_name') or fund_data.get('nav')),
        }
        return validation


def main():
    """Main function to run the scraper"""
    scraper = GrowwMutualFundScraper()
    
    # Example: Scrape a single fund
    test_url = "https://groww.in/mutual-funds/icici-prudential-banking-psu-debt-fund-direct-growth"
    print("Testing scraper on single fund...")
    fund_data = scraper.scrape_fund_page(test_url)
    
    if fund_data:
        print("\nScraped Data:")
        print(json.dumps(fund_data, indent=2))
        
        # Validate
        validation = scraper.validate_data(fund_data)
        print("\nValidation Results:")
        print(json.dumps(validation, indent=2))
    
    # Example: Scrape category
    category_url = "https://groww.in/mutual-funds/category/best-banking-and-psu-mutual-funds"
    print(f"\n\nScraping category: {category_url}")
    all_funds = scraper.scrape_category(category_url)
    
    if all_funds:
        scraper.save_data(all_funds, 'groww_banking_psu_funds.json')
        print(f"\nSuccessfully scraped {len(all_funds)} funds")


if __name__ == "__main__":
    main()


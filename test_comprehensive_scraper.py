"""
Test comprehensive data scraping for HDFC Mid Cap Fund and validate results
"""

import json
from groww_scraper import GrowwMutualFundScraper

def test_hdfc_midcap_scraping():
    """Test scraping HDFC Mid Cap Fund Direct Growth"""
    scraper = GrowwMutualFundScraper()
    
    # Test URL from your example
    test_url = "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth"
    
    print("="*80)
    print("TESTING COMPREHENSIVE DATA EXTRACTION")
    print("="*80)
    print(f"\nScraping: {test_url}\n")
    
    # Scrape the fund
    fund_data = scraper.scrape_fund_page(test_url)
    
    if not fund_data:
        print("❌ Failed to scrape fund data!")
        return False
    
    print("\n" + "="*80)
    print("EXTRACTED DATA")
    print("="*80)
    
    # Validate key fields
    validations = {
        'source_url': test_url,
        'scheme_name': 'HDFC Mid Cap Fund Direct Growth',
        'expense_ratio': '0.7%',
        'exit_load': 'Exit load of 1% if redeemed within 1 year',
        'stamp_duty': '0.005%',
    }
    
    print(f"\n✓ Source URL: {fund_data.get('source_url')}")
    print(f"✓ Scheme Name: {fund_data.get('scheme_name')}")
    print(f"✓ NAV: {fund_data.get('nav')}")
    print(f"✓ Expense Ratio: {fund_data.get('expense_ratio')}")
    print(f"✓ Exit Load: {fund_data.get('exit_load')}")
    print(f"✓ Stamp Duty: {fund_data.get('stamp_duty')}")
    print(f"✓ Tax Implications: {fund_data.get('tax_implications')}")
    print(f"✓ Riskometer: {fund_data.get('riskometer')}")
    print(f"✓ Benchmark: {fund_data.get('benchmark')}")
    print(f"✓ Fund Size: {fund_data.get('fund_size')}")
    print(f"✓ Fund Manager: {fund_data.get('fund_manager')}")
    
    # Minimum investment
    min_inv = fund_data.get('minimum_investment', {})
    print(f"\n📊 Minimum Investment:")
    print(f"   - Min SIP: ₹{min_inv.get('min_sip', 'N/A')}")
    print(f"   - Min Lumpsum: ₹{min_inv.get('min_lumpsum', 'N/A')}")
    print(f"   - First Investment: ₹{min_inv.get('first_investment', 'N/A')}")
    print(f"   - Subsequent: ₹{min_inv.get('subsequent_investment', 'N/A')}")
    
    # Holdings
    holdings = fund_data.get('holdings', [])
    print(f"\n📈 Holdings ({len(holdings)} found):")
    for i, holding in enumerate(holdings[:5], 1):
        print(f"   {i}. {holding.get('name', 'N/A')} - {holding.get('assets', 'N/A')}")
    if len(holdings) > 5:
        print(f"   ... and {len(holdings) - 5} more")
    
    # Debt/Cash Analysis
    debt_cash = fund_data.get('debt_cash_analysis', {})
    print(f"\n💰 Debt & Cash Analysis:")
    print(f"   - Total Debt: {debt_cash.get('total_debt', 'N/A')}")
    print(f"   - Total Cash: {debt_cash.get('total_cash', 'N/A')}")
    
    # Sector Allocation
    sectors = fund_data.get('sector_allocation', {})
    if sectors:
        print(f"\n🏭 Sector Allocation:")
        for sector, percentage in list(sectors.items())[:5]:
            print(f"   - {sector}: {percentage}")
    
    # Additional Links
    links = fund_data.get('additional_links', {})
    print(f"\n🔗 Additional Resources:")
    if links.get('factsheet_url'):
        print(f"   - Factsheet: {links['factsheet_url']}")
    if links.get('kim_url'):
        print(f"   - KIM: {links['kim_url']}")
    if links.get('sid_url'):
        print(f"   - SID: {links['sid_url']}")
    
    # Save to JSON
    output_file = 'hdfc_midcap_comprehensive_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fund_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full data saved to: {output_file}")
    
    # Validation
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    
    validation_passed = True
    
    # Check if expense ratio matches expected
    if fund_data.get('expense_ratio'):
        if '0.7' in fund_data.get('expense_ratio', ''):
            print("✅ Expense ratio validation PASSED (contains 0.7%)")
        else:
            print(f"⚠️  Expense ratio: Got '{fund_data.get('expense_ratio')}', expected to contain 0.7%")
    else:
        print("❌ Expense ratio: NOT FOUND")
        validation_passed = False
    
    # Check exit load
    if fund_data.get('exit_load'):
        if '1%' in fund_data.get('exit_load', '') and 'year' in fund_data.get('exit_load', '').lower():
            print("✅ Exit load validation PASSED (contains 1% within 1 year)")
        else:
            print(f"⚠️  Exit load: Got '{fund_data.get('exit_load')}'")
    else:
        print("❌ Exit load: NOT FOUND")
        validation_passed = False
    
    # Check stamp duty
    if fund_data.get('stamp_duty'):
        if '0.005' in fund_data.get('stamp_duty', ''):
            print("✅ Stamp duty validation PASSED (contains 0.005%)")
        else:
            print(f"⚠️  Stamp duty: Got '{fund_data.get('stamp_duty')}', expected to contain 0.005%")
    else:
        print("❌ Stamp duty: NOT FOUND")
        validation_passed = False
    
    # Check tax implications
    if fund_data.get('tax_implications'):
        tax_text = fund_data.get('tax_implications', '').lower()
        if 'redeem' in tax_text and 'taxed' in tax_text:
            print("✅ Tax implications validation PASSED (contains redemption tax info)")
        else:
            print(f"⚠️  Tax implications found but may be incomplete")
    else:
        print("❌ Tax implications: NOT FOUND")
        validation_passed = False
    
    # Check holdings
    if len(holdings) > 0:
        print(f"✅ Holdings validation PASSED ({len(holdings)} holdings extracted)")
    else:
        print("❌ Holdings: NOT FOUND")
        validation_passed = False
    
    # Check source URL is valid
    if scraper.validate_url(fund_data.get('source_url', '')):
        print("✅ Source URL validation PASSED")
    else:
        print("❌ Source URL validation FAILED")
        validation_passed = False
    
    print("\n" + "="*80)
    if validation_passed:
        print("✅ OVERALL VALIDATION: PASSED")
    else:
        print("⚠️  OVERALL VALIDATION: PARTIAL - Some fields missing")
    print("="*80)
    
    return fund_data


def test_backend_integration(fund_data):
    """Test the scraped data with the backend"""
    print("\n" + "="*80)
    print("TESTING BACKEND INTEGRATION")
    print("="*80)
    
    try:
        from data_storage import MutualFundDataStore
        
        # Save to database
        store = MutualFundDataStore()
        
        # Convert to the format expected by data_storage
        scheme_data = {
            'id': fund_data.get('scheme_name', '').lower().replace(' ', '-'),
            'scheme_name': fund_data.get('scheme_name'),
            'category': fund_data.get('category'),
            'source_url': fund_data.get('source_url'),
            'facts': {
                'nav': fund_data.get('nav'),
                'expense_ratio': fund_data.get('expense_ratio'),
                'exit_load': fund_data.get('exit_load'),
                'stamp_duty': fund_data.get('stamp_duty'),
                'tax_implications': fund_data.get('tax_implications'),
                'minimum_sip': fund_data['minimum_investment'].get('min_sip'),
                'minimum_lumpsum': fund_data['minimum_investment'].get('min_lumpsum'),
                'first_investment': fund_data['minimum_investment'].get('first_investment'),
                'subsequent_investment': fund_data['minimum_investment'].get('subsequent_investment'),
                'lock_in': fund_data.get('lock_in'),
                'riskometer': fund_data.get('riskometer'),
                'benchmark': fund_data.get('benchmark'),
                'fund_size': fund_data.get('fund_size'),
                'fund_manager': fund_data.get('fund_manager'),
                'total_debt': fund_data['debt_cash_analysis'].get('total_debt'),
                'total_cash': fund_data['debt_cash_analysis'].get('total_cash'),
            }
        }
        
        # Save
        store.save_scheme(scheme_data)
        print("✅ Successfully saved to backend database")
        
        # Retrieve and verify
        retrieved = store.find_scheme_by_name(fund_data.get('scheme_name'))
        if retrieved:
            print("✅ Successfully retrieved from backend database")
            print(f"   - Expense Ratio: {retrieved['facts'].get('expense_ratio')}")
            print(f"   - Exit Load: {retrieved['facts'].get('exit_load')}")
            print(f"   - Stamp Duty: {retrieved['facts'].get('stamp_duty')}")
            return True
        else:
            print("❌ Failed to retrieve from backend")
            return False
            
    except Exception as e:
        print(f"❌ Backend integration error: {e}")
        return False


if __name__ == "__main__":
    # Test scraping
    fund_data = test_hdfc_midcap_scraping()
    
    if fund_data:
        # Test backend integration
        test_backend_integration(fund_data)
        
        print("\n✅ All tests completed!")
    else:
        print("\n❌ Scraping failed!")

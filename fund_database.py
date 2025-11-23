"""
Mutual Fund Database - Stores scraped data in structured JSON format
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class FundDatabase:
    """Database for storing mutual fund facts"""
    
    def __init__(self, db_file: str = "mutual_funds_db.json"):
        self.db_file = Path(db_file)
        self.funds = []
        self.load_database()
    
    def load_database(self):
        """Load existing database or create new one"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.funds = json.load(f)
                print(f"✅ Loaded {len(self.funds)} funds from database")
            except Exception as e:
                print(f"❌ Error loading database: {e}")
                self.funds = []
        else:
            print("📝 Creating new database")
            self.funds = []
    
    def add_fund(self, fund_data: Dict):
        """
        Add fund to database
        
        Expected format:
        {
            "scheme_name": "...",
            "expense_ratio": "1.04%" or "Information not available",
            "lock_in": "3 years" or "Information not available",
            "minimum_sip": "₹500" or "Information not available",
            "exit_load": "1% if redeemed within 1 year" or "Information not available",
            "riskometer": "High" or "Information not available",
            "benchmark": "NIFTY 50" or "Information not available",
            "nav": "₹42.58" or "Information not available",
            "fund_manager": "..." or "Information not available",
            "source_url": "https://groww.in/mutual-funds/..."
        }
        """
        # Check for duplicates by source URL
        existing = self.find_by_url(fund_data.get('source_url'))
        
        if existing:
            # Update existing record
            idx = self.funds.index(existing)
            self.funds[idx] = fund_data
            print(f"🔄 Updated: {fund_data.get('scheme_name')}")
        else:
            # Add new record
            self.funds.append(fund_data)
            print(f"✅ Added: {fund_data.get('scheme_name')}")
    
    def save_database(self):
        """Save database to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.funds, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(self.funds)} funds to {self.db_file}")
        except Exception as e:
            print(f"❌ Error saving database: {e}")
    
    def find_by_name(self, scheme_name: str) -> Optional[Dict]:
        """Find fund by scheme name (case-insensitive partial match)"""
        scheme_name_lower = scheme_name.lower()
        
        # First try exact match
        for fund in self.funds:
            if fund.get('scheme_name', '').lower() == scheme_name_lower:
                return fund
        
        # Then try partial match
        for fund in self.funds:
            if scheme_name_lower in fund.get('scheme_name', '').lower():
                return fund
        
        return None
    
    def find_by_url(self, url: str) -> Optional[Dict]:
        """Find fund by source URL"""
        for fund in self.funds:
            if fund.get('source_url') == url:
                return fund
        return None
    
    def get_field_value(self, scheme_name: str, field: str) -> Optional[str]:
        """
        Get specific field value for a fund
        
        Args:
            scheme_name: Name of the scheme
            field: Field name (expense_ratio, lock_in, etc.)
        
        Returns:
            Field value or None if not found
        """
        fund = self.find_by_name(scheme_name)
        
        if not fund:
            return None
        
        return fund.get(field)
    
    def get_all_funds(self) -> List[Dict]:
        """Get all funds in database"""
        return self.funds
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        total_funds = len(self.funds)
        
        fields_to_check = [
            'expense_ratio', 'lock_in', 'minimum_sip', 'exit_load',
            'riskometer', 'benchmark', 'nav', 'fund_manager'
        ]
        
        field_stats = {}
        for field in fields_to_check:
            available = sum(
                1 for fund in self.funds 
                if fund.get(field) and fund.get(field) != "Information not available"
            )
            field_stats[field] = {
                'available': available,
                'percentage': (available / total_funds * 100) if total_funds > 0 else 0
            }
        
        return {
            'total_funds': total_funds,
            'field_completeness': field_stats,
            'last_updated': datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Test database
    db = FundDatabase()
    
    # Add sample fund
    sample_fund = {
        "scheme_name": "Axis Bluechip Fund Direct Growth",
        "expense_ratio": "1.01%",
        "lock_in": "Information not available",
        "minimum_sip": "₹500",
        "exit_load": "1% if redeemed within 1 year",
        "riskometer": "Very High",
        "benchmark": "NIFTY 50",
        "nav": "₹42.58",
        "fund_manager": "Shreyash Devalkar",
        "source_url": "https://groww.in/mutual-funds/axis-bluechip-fund-direct-growth"
    }
    
    db.add_fund(sample_fund)
    db.save_database()
    
    # Test retrieval
    print("\n" + "="*60)
    print("Testing retrieval:")
    found = db.find_by_name("Axis Bluechip")
    if found:
        print(f"Found: {found['scheme_name']}")
        print(f"Expense Ratio: {found['expense_ratio']}")
        print(f"Source: {found['source_url']}")
    
    # Show statistics
    print("\n" + "="*60)
    print("Database Statistics:")
    stats = db.get_statistics()
    print(json.dumps(stats, indent=2))

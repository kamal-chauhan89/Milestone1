"""
Data Storage Module for Groww Mutual Fund FAQ Assistant
Organizes and stores scraped data in a structured format for RAG
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class MutualFundDataStore:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Storage paths
        self.schemes_file = self.data_dir / "schemes.json"
        self.index_file = self.data_dir / "index.json"
        self.embeddings_dir = self.data_dir / "embeddings"
        self.embeddings_dir.mkdir(exist_ok=True)
    
    def load_scraped_data(self, json_file: str) -> List[Dict]:
        """Load scraped data from JSON file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both direct list and wrapped format
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'schemes' in data:
            return data['schemes']
        elif isinstance(data, dict) and 'data' in data:
            return data['data']
        else:
            return []
    
    def normalize_scheme_data(self, scheme: Dict) -> Dict:
        """Normalize and structure scheme data for storage"""
        normalized = {
            'id': self._generate_scheme_id(scheme),
            'scheme_name': scheme.get('scheme_name', 'Unknown'),
            'source_url': scheme.get('source_url', ''),
            'category': scheme.get('category', 'Unknown'),
            'last_updated': scheme.get('scraped_at', datetime.now().isoformat()),
            
            # Core facts
            'facts': {
                'expense_ratio': scheme.get('expense_ratio'),
                'exit_load': scheme.get('exit_load'),
                'minimum_sip': scheme.get('minimum_investment', {}).get('min_sip'),
                'minimum_lumpsum': scheme.get('minimum_investment', {}).get('min_lumpsum'),
                'first_investment': scheme.get('minimum_investment', {}).get('first_investment'),
                'subsequent_investment': scheme.get('minimum_investment', {}).get('subsequent_investment'),
                'lock_in': scheme.get('lock_in'),
                'riskometer': scheme.get('riskometer'),
                'benchmark': scheme.get('benchmark'),
                'nav': scheme.get('nav'),
                'fund_size': scheme.get('fund_size'),
                'fund_manager': scheme.get('fund_manager'),
            },
            
            # Holdings and analysis
            'holdings': scheme.get('holdings', []),
            'sector_allocation': scheme.get('sector_allocation', {}),
            'debt_cash_analysis': scheme.get('debt_cash_analysis', {}),
            
            # Additional resources
            'return_calculator': scheme.get('return_calculator', {}),
            'additional_links': scheme.get('additional_links', {}),
        }
        
        return normalized
    
    def _generate_scheme_id(self, scheme: Dict) -> str:
        """Generate unique ID for scheme"""
        scheme_name = scheme.get('scheme_name', 'unknown')
        # Create ID from scheme name
        scheme_id = scheme_name.lower().replace(' ', '-').replace('&', 'and')
        scheme_id = ''.join(c for c in scheme_id if c.isalnum() or c in ('-', '_'))
        return scheme_id[:100]  # Limit length
    
    def create_searchable_text(self, scheme: Dict) -> str:
        """Create searchable text representation of scheme"""
        facts = scheme.get('facts', {})
        text_parts = []
        
        # Scheme name
        text_parts.append(f"Scheme: {scheme.get('scheme_name', 'Unknown')}")
        
        # Category
        if scheme.get('category'):
            text_parts.append(f"Category: {scheme.get('category')}")
        
        # Expense ratio
        if facts.get('expense_ratio'):
            text_parts.append(f"Expense ratio: {facts['expense_ratio']}")
        
        # Exit load
        if facts.get('exit_load'):
            text_parts.append(f"Exit load: {facts['exit_load']}")
        
        # Minimum SIP
        if facts.get('minimum_sip'):
            text_parts.append(f"Minimum SIP: ₹{facts['minimum_sip']}")
        
        # Minimum lumpsum
        if facts.get('minimum_lumpsum'):
            text_parts.append(f"Minimum lumpsum: ₹{facts['minimum_lumpsum']}")
        
        # Lock-in period
        if facts.get('lock_in'):
            text_parts.append(f"Lock-in period: {facts['lock_in']}")
            if 'ELSS' in str(facts.get('lock_in', '')).upper():
                text_parts.append("ELSS funds have a 3-year lock-in period")
        
        # Riskometer
        if facts.get('riskometer'):
            text_parts.append(f"Riskometer: {facts['riskometer']}")
        
        # Benchmark
        if facts.get('benchmark'):
            text_parts.append(f"Benchmark: {facts['benchmark']}")
        
        # Fund manager
        if facts.get('fund_manager'):
            text_parts.append(f"Fund manager: {facts['fund_manager']}")
        
        return "\n".join(text_parts)
    
    def store_schemes(self, schemes: List[Dict], overwrite: bool = True):
        """Store normalized schemes to JSON"""
        normalized_schemes = []
        
        print(f"Normalizing {len(schemes)} schemes...")
        for scheme in schemes:
            normalized = self.normalize_scheme_data(scheme)
            normalized_schemes.append(normalized)
        
        # Save schemes
        with open(self.schemes_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_schemes, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Stored {len(normalized_schemes)} schemes to {self.schemes_file}")
        
        # Create index
        self._create_index(normalized_schemes)
        
        return normalized_schemes
    
    def _create_index(self, schemes: List[Dict]):
        """Create search index for quick lookups"""
        index = {
            'created_at': datetime.now().isoformat(),
            'total_schemes': len(schemes),
            'scheme_names': {},
            'categories': {},
            'amcs': {},
        }
        
        for scheme in schemes:
            scheme_id = scheme['id']
            scheme_name = scheme['scheme_name']
            
            # Index by scheme name (case-insensitive)
            name_key = scheme_name.lower()
            if name_key not in index['scheme_names']:
                index['scheme_names'][name_key] = []
            index['scheme_names'][name_key].append(scheme_id)
            
            # Index by category
            category = scheme.get('category', 'Unknown')
            if category not in index['categories']:
                index['categories'][category] = []
            index['categories'][category].append(scheme_id)
        
        # Save index
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created index with {len(index['scheme_names'])} unique scheme names")
    
    def load_schemes(self) -> List[Dict]:
        """Load stored schemes"""
        if not self.schemes_file.exists():
            return []
        
        with open(self.schemes_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_scheme_by_name(self, scheme_name: str) -> Optional[Dict]:
        """Find scheme by name (fuzzy matching)"""
        schemes = self.load_schemes()
        scheme_name_lower = scheme_name.lower()
        
        # Exact match first
        for scheme in schemes:
            if scheme['scheme_name'].lower() == scheme_name_lower:
                return scheme
        
        # Partial match
        for scheme in schemes:
            if scheme_name_lower in scheme['scheme_name'].lower():
                return scheme
        
        # Word match
        query_words = set(scheme_name_lower.split())
        for scheme in schemes:
            scheme_words = set(scheme['scheme_name'].lower().split())
            if query_words.issubset(scheme_words):
                return scheme
        
        return None


def main():
    """Store scraped data"""
    print("=" * 60)
    print("MUTUAL FUND DATA STORAGE")
    print("=" * 60)
    
    # Initialize storage
    store = MutualFundDataStore(data_dir="data")
    
    # Load scraped data
    scraped_file = "groww_all_funds_scraped.json"
    
    if not os.path.exists(scraped_file):
        print(f"\n[ERROR] Scraped data file not found: {scraped_file}")
        print("Please run the scraper first:")
        print("  python scrape_all_automated.py")
        return
    
    print(f"\nLoading scraped data from: {scraped_file}")
    schemes = store.load_scraped_data(scraped_file)
    
    if not schemes:
        print("[ERROR] No schemes found in scraped data")
        return
    
    print(f"Found {len(schemes)} schemes to store")
    
    # Store schemes
    normalized_schemes = store.store_schemes(schemes)
    
    print(f"\n✅ Data storage complete!")
    print(f"   Stored: {len(normalized_schemes)} schemes")
    print(f"   Location: {store.data_dir}")
    print(f"\nNext step: Run the FAQ assistant backend")


if __name__ == "__main__":
    main()


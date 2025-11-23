"""
FAQ Backend API - Facts-only mutual fund query system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from fund_database import FundDatabase
import re
from typing import Dict, Optional, Tuple


import os

app = Flask(__name__)
CORS(app)

# Initialize database
db = FundDatabase()


class QueryProcessor:
    """Process user queries and extract fund name + question type"""
    
    FIELD_KEYWORDS = {
        'expense_ratio': ['expense ratio', 'expense', 'fees', 'charges'],
        'exit_load': ['exit load', 'exit charge', 'redemption charge'],
        'minimum_sip': ['minimum sip', 'min sip', 'sip amount', 'sip minimum'],
        'lock_in': ['lock-in', 'lock in', 'lockin', 'elss lock', 'holding period'],
        'riskometer': ['riskometer', 'risk level', 'risk', 'risk meter'],
        'benchmark': ['benchmark', 'index'],
        'nav': ['nav', 'net asset value', 'current value', 'price'],
        'fund_manager': ['fund manager', 'manager', 'who manages'],
        'stamp_duty': ['stamp duty', 'stamp'],
        'tax_implications': ['tax', 'taxation', 'tax implication'],
    }
    
    OPINION_KEYWORDS = [
        'should i', 'is it good', 'recommend', 'best', 'better',
        'invest', 'portfolio', 'suggest', 'advice', 'which one'
    ]
    
    def extract_fund_name(self, query: str) -> Optional[str]:
        """Extract fund name from query"""
        query_lower = query.lower()
        
        # Common fund name patterns to look for
        fund_keywords = [
            'hdfc', 'icici', 'sbi', 'axis', 'kotak', 'reliance', 'tata', 'birla',
            'mid cap', 'large cap', 'small cap', 'bluechip', 'equity', 'debt',
            'hybrid', 'elss', 'tax saver', 'flexi cap', 'focused', 'balanced'
        ]
        
        # Try to find fund name by searching database
        for fund in db.get_all_funds():
            fund_name = fund.get('scheme_name', '')
            fund_name_lower = fund_name.lower()
            
            # Check if fund name is in query
            if fund_name_lower in query_lower:
                return fund_name
            
            # Check if significant parts of fund name are in query
            name_parts = fund_name_lower.split()
            
            # Need at least 2 words to match (to avoid false positives)
            if len(name_parts) >= 2:
                matched_parts = sum(1 for part in name_parts if part in query_lower)
                
                # If most of the fund name is in query, it's a match
                if matched_parts >= min(2, len(name_parts) - 1):
                    return fund_name
        
        return None
    
    def extract_question_type(self, query: str) -> Optional[str]:
        """Identify what field the user is asking about"""
        query_lower = query.lower()
        
        for field, keywords in self.FIELD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return field
        
        return None
    
    def is_opinion_question(self, query: str) -> bool:
        """Check if query is asking for opinion/advice"""
        query_lower = query.lower()
        
        for keyword in self.OPINION_KEYWORDS:
            if keyword in query_lower:
                return True
        
        return False
    
    def process_query(self, query: str) -> Tuple[Optional[str], Optional[str], bool]:
        """
        Process query and return (fund_name, field, is_opinion)
        """
        # Check for opinion first
        if self.is_opinion_question(query):
            return None, None, True
        
        # Extract fund name and field
        fund_name = self.extract_fund_name(query)
        field = self.extract_question_type(query)
        
        return fund_name, field, False


processor = QueryProcessor()


@app.route('/query', methods=['POST'])
def answer_query():
    """
    Main query endpoint
    
    Request:
        {
            "query": "Expense ratio of Axis Bluechip Fund?"
        }
    
    Response:
        {
            "answer": "The expense ratio of Axis Bluechip Fund is 1.01%.",
            "source": "https://groww.in/mutual-funds/axis-bluechip-fund-direct-growth",
            "fund_name": "Axis Bluechip Fund Direct Growth"
        }
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Query is required'
            }), 400
        
        # Process query
        fund_name, field, is_opinion = processor.process_query(query)
        
        # Refuse opinion questions
        if is_opinion:
            return jsonify({
                'answer': 'I provide only facts. For investment advice, please contact a financial adviser.',
                'is_opinion': True
            })
        
        # Check if fund found
        if not fund_name:
            return jsonify({
                'answer': 'Fund not found. Please provide a valid mutual fund name.',
                'error': 'fund_not_found'
            })
        
        # Get fund data
        fund = db.find_by_name(fund_name)
        
        if not fund:
            return jsonify({
                'answer': 'Fund not found in database.',
                'error': 'fund_not_found'
            })
        
        # Check if field identified
        if not field:
            # Provide general info
            answer = f"I found information about {fund['scheme_name']}. What would you like to know? (expense ratio, exit load, minimum SIP, lock-in, riskometer, benchmark, NAV, etc.)"
            
            return jsonify({
                'answer': answer,
                'source': fund['source_url'],
                'fund_name': fund['scheme_name']
            })
        
        # Get field value
        value = fund.get(field)
        
        if not value or value == "Information not available":
            # Data not available
            answer = f"Information not available. See {fund['scheme_name']} factsheet."
            
            return jsonify({
                'answer': answer,
                'source': fund['source_url'],
                'fund_name': fund['scheme_name'],
                'field': field,
                'data_available': False
            })
        
        # Construct answer with precise value and citation
        field_label = field.replace('_', ' ').title()
        answer = f"The {field_label.lower()} of {fund['scheme_name']} is {value}."
        
        return jsonify({
            'answer': answer,
            'source': fund['source_url'],
            'fund_name': fund['scheme_name'],
            'field': field,
            'value': value,
            'data_available': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/funds', methods=['GET'])
def list_funds():
    """List all available funds"""
    funds = db.get_all_funds()
    
    return jsonify({
        'total': len(funds),
        'funds': [
            {
                'scheme_name': f['scheme_name'],
                'source_url': f['source_url']
            }
            for f in funds
        ]
    })


@app.route('/fund/<path:fund_name>', methods=['GET'])
def get_fund_details(fund_name: str):
    """Get all details for a specific fund"""
    fund = db.find_by_name(fund_name)
    
    if not fund:
        return jsonify({
            'error': 'Fund not found'
        }), 404
    
    return jsonify(fund)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    stats = db.get_statistics()
    
    return jsonify({
        'status': 'healthy',
        'database': stats,
        'message': f'API is running with {stats["total_funds"]} mutual funds loaded'
    })


@app.route('/examples', methods=['GET'])
def get_examples():
    """Get example questions"""
    examples = [
        "Expense ratio of HDFC Mid Cap Fund?",
        "ELSS lock-in period?",
        "Minimum SIP for SBI Bluechip Fund?"
    ]
    
    return jsonify({
        'examples': examples,
        'note': 'Facts-only. No investment advice.'
    })


if __name__ == '__main__':
    print("="*80)
    print("MUTUAL FUND FAQ BACKEND API")
    print("="*80)
    print(f"Database loaded: {len(db.get_all_funds())} funds")
    print("\nEndpoints:")
    print("  POST /query - Answer a query")
    print("  GET /funds - List all funds")
    print("  GET /fund/<name> - Get fund details")
    print("  GET /examples - Get example questions")
    print("  GET /health - Health check")
    print("\nExample query:")
    print('  curl -X POST http://localhost:5000/query \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"query": "Expense ratio of Axis Bluechip Fund?"}\'')
    print("="*80)
    
    # Use PORT from environment variable for Railway deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

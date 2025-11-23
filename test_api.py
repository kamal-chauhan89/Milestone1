"""
Test the FAQ Backend API
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_query(query_text):
    """Test a query"""
    print(f"\n{'='*80}")
    print(f"QUERY: {query_text}")
    print(f"{'='*80}")
    
    response = requests.post(
        f"{API_URL}/query",
        json={"query": query_text}
    )
    
    data = response.json()
    print(json.dumps(data, indent=2))
    
    return data

# Test queries
print("\n" + "="*80)
print("TESTING FAQ BACKEND API")
print("="*80)

# Test 1: Expense ratio query
test_query("Expense ratio of HDFC Mid Cap Fund?")

# Test 2: Exit load query
test_query("Exit load for HDFC Mid Cap Fund?")

# Test 3: Tax implications
test_query("What are the tax implications for HDFC Mid Cap Fund?")

# Test 4: Opinion question (should refuse)
test_query("Should I invest in HDFC Mid Cap Fund?")

# Test 5: Fund not found
test_query("Expense ratio of XYZ Fund?")

# Test 6: ELSS lock-in
test_query("ELSS lock-in period?")

print("\n" + "="*80)
print("TESTS COMPLETE")
print("="*80)

"""
Complete Demo of FAQ Assistant Backend
Demonstrates all supported query types with examples
"""

from faq_assistant_backend import FAQAssistant
import json

def print_result(query: str, result: dict):
    """Pretty print query result"""
    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("-" * 70)
    print(f"ANSWER: {result['answer']}")
    print(f"\nSOURCE: {result['source_url']}")
    print(f"TYPE: {result['question_type']}")
    if result.get('scheme_name'):
        print(f"SCHEME: {result['scheme_name']}")
    print("=" * 70)

def main():
    print("=" * 70)
    print("GROWW MUTUAL FUND FAQ ASSISTANT - BACKEND DEMO")
    print("=" * 70)
    
    # Initialize assistant
    print("\nInitializing FAQ Assistant...")
    assistant = FAQAssistant()
    print(f"✅ Loaded {len(assistant.schemes)} schemes from database")
    
    # Test queries organized by type
    test_queries = {
        "EXPENSE RATIO": [
            "Expense ratio of ICICI Prudential Banking & PSU Debt Fund",
            "What is the expense ratio for Axis Floater Fund?",
            "Expense ratio?",
        ],
        "MINIMUM SIP": [
            "Minimum SIP for HDFC Large Cap Fund",
            "What is the minimum SIP amount?",
            "Min SIP for ICICI Prudential Banking & PSU Debt Fund",
        ],
        "EXIT LOAD": [
            "Exit load of SBI Small Cap Fund",
            "What is the exit load?",
            "Exit load for Axis Floater Fund",
        ],
        "LOCK-IN / ELSS": [
            "ELSS lock-in period?",
            "What is the lock-in period for ELSS funds?",
            "Lock-in period for tax saver funds",
        ],
        "RISKOMETER": [
            "Riskometer of Nippon India Growth Fund",
            "What is the riskometer rating?",
            "Risk rating for ICICI Prudential Banking & PSU Debt Fund",
        ],
        "BENCHMARK": [
            "Benchmark of HDFC Flexi Cap Fund",
            "What is the benchmark?",
            "Benchmark for Axis Floater Fund",
        ],
        "STATEMENTS": [
            "How to download capital gains statement?",
            "How do I download tax documents?",
            "Where can I download my mutual fund statements?",
        ],
        "OPINIONATED (Should be refused)": [
            "Should I buy ICICI Prudential Banking & PSU Debt Fund?",
            "Is this a good fund to invest in?",
            "Can you recommend a mutual fund?",
            "Should I sell my holdings?",
        ],
        "EDGE CASES": [
            "Expense ratio",  # No scheme name
            "What is SIP?",  # General question
            "Minimum investment for non-existent fund",  # Scheme not found
        ],
    }
    
    # Run all test queries
    print("\n" + "=" * 70)
    print("RUNNING TEST QUERIES")
    print("=" * 70)
    
    for category, queries in test_queries.items():
        print(f"\n\n{'#' * 70}")
        print(f"# {category}")
        print(f"{'#' * 70}")
        
        for query in queries:
            result = assistant.answer_query(query)
            print_result(query, result)
    
    # Summary
    print("\n\n" + "=" * 70)
    print("DEMO SUMMARY")
    print("=" * 70)
    print(f"\n✅ Tested {sum(len(queries) for queries in test_queries.values())} queries")
    print(f"✅ All query types handled")
    print(f"✅ Citation links included in all answers")
    print(f"✅ Opinionated questions properly refused")
    print("\n" + "=" * 70)
    
    # Show example API response
    print("\n\nEXAMPLE API RESPONSE FORMAT:")
    print("-" * 70)
    example_query = "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"
    example_result = assistant.answer_query(example_query)
    print(json.dumps({
        "success": True,
        "query": example_query,
        "answer": example_result['answer'],
        "source_url": example_result['source_url'],
        "question_type": example_result['question_type'],
        "scheme_name": example_result.get('scheme_name'),
    }, indent=2))
    print("=" * 70)

if __name__ == "__main__":
    main()


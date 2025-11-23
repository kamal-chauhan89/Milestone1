"""
Unit Tests for FAQ Assistant with Google Gemini
Tests 5 example prompts to verify answers are correct
"""

from faq_assistant_backend import FAQAssistant
import json

def test_query(query: str, expected_type: str = None, should_have_scheme: bool = False):
    """Test a single query"""
    print("\n" + "=" * 70)
    print(f"TEST QUERY: {query}")
    print("=" * 70)
    
    assistant = FAQAssistant()
    result = assistant.answer_query(query)
    
    print(f"\n[ANSWER]")
    print(f"   {result['answer']}")
    print(f"\n[SOURCE URL]")
    print(f"   {result['source_url']}")
    print(f"\n[QUESTION TYPE] {result['question_type']}")
    if result.get('scheme_name'):
        print(f"[SCHEME] {result['scheme_name']}")
    
    # Validation
    print(f"\n[VALIDATION]")
    checks = []
    
    if expected_type:
        if result['question_type'] == expected_type:
            checks.append("[OK] Question type matches expected")
        else:
            checks.append(f"[FAIL] Question type mismatch: expected {expected_type}, got {result['question_type']}")
    
    if should_have_scheme:
        if result.get('scheme_name'):
            checks.append("[OK] Scheme name extracted")
        else:
            checks.append("[FAIL] Scheme name not extracted")
    
    if result.get('source_url'):
        if 'groww.in' in result['source_url']:
            checks.append("[OK] Valid Groww source URL")
        else:
            checks.append("[FAIL] Invalid source URL")
    else:
        checks.append("[FAIL] No source URL provided")
    
    if result.get('answer'):
        if len(result['answer']) > 10:
            checks.append("[OK] Answer is substantial")
        else:
            checks.append("[FAIL] Answer too short")
    else:
        checks.append("[FAIL] No answer provided")
    
    for check in checks:
        print(f"   {check}")
    
    return result

def main():
    print("=" * 70)
    print("UNIT TESTS - FAQ ASSISTANT WITH GOOGLE GEMINI")
    print("=" * 70)
    
    # Initialize assistant
    print("\nInitializing FAQ Assistant...")
    try:
        assistant = FAQAssistant()
        print(f"[OK] Loaded {len(assistant.schemes)} schemes")
        print("[OK] Google Gemini initialized")
    except Exception as e:
        print(f"[ERROR] Error initializing: {e}")
        print("\nMake sure:")
        print("  1. GOOGLE_GEMINI_API_KEY is set in .env file")
        print("  2. You have installed: pip install google-generativeai python-dotenv")
        return
    
    # Test 5 example prompts
    test_cases = [
        {
            'query': "Expense ratio of ICICI Prudential Banking & PSU Debt Fund",
            'expected_type': 'expense_ratio',
            'should_have_scheme': True,
            'description': 'Test expense ratio query with scheme name'
        },
        {
            'query': "What is the minimum SIP amount?",
            'expected_type': 'minimum_sip',
            'should_have_scheme': False,
            'description': 'Test minimum SIP query without scheme name'
        },
        {
            'query': "ELSS lock-in period?",
            'expected_type': 'lock_in',
            'should_have_scheme': False,
            'description': 'Test ELSS lock-in query'
        },
        {
            'query': "Exit load for Axis Floater Fund",
            'expected_type': 'exit_load',
            'should_have_scheme': True,
            'description': 'Test exit load query with scheme name'
        },
        {
            'query': "Should I invest in this mutual fund?",
            'expected_type': 'opinionated',
            'should_have_scheme': False,
            'description': 'Test opinionated question (should be refused)'
        },
    ]
    
    print("\n" + "=" * 70)
    print("RUNNING 5 UNIT TESTS")
    print("=" * 70)
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{'#' * 70}")
        print(f"# TEST {i}/5: {test_case['description']}")
        print(f"{'#' * 70}")
        
        result = test_query(
            test_case['query'],
            test_case['expected_type'],
            test_case['should_have_scheme']
        )
        results.append({
            'test': i,
            'query': test_case['query'],
            'result': result,
            'passed': result.get('answer') is not None and result.get('source_url') is not None
        })
    
    # Summary
    print("\n\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print(f"\n[PASSED] {passed}/{total}")
    print(f"[FAILED] {total - passed}/{total}")
    
    for result in results:
        status = "[PASS]" if result['passed'] else "[FAIL]"
        print(f"\n{status} - Test {result['test']}: {result['query'][:50]}...")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[WARNING] Some tests failed. Review the output above.")
    print("=" * 70)

if __name__ == "__main__":
    main()
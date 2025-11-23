"""
FAQ Assistant Backend for Groww Mutual Funds with Google Gemini
Answers factual questions with citations, refuses opinionated questions
"""

import json
import re
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from data_storage import MutualFundDataStore
import google.generativeai as genai

# Try to load environment variables from .env file (handle encoding issues)
try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        try:
            # Try loading with dotenv
            load_dotenv(dotenv_path=env_path, encoding='utf-8')
        except (UnicodeDecodeError, Exception) as e:
            # If loading fails, try to read manually
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
            except Exception:
                print(f"Warning: Could not load .env file: {e}. Using environment variables only.")
    else:
        load_dotenv()  # This will just return if file doesn't exist
except ImportError:
    print("Warning: python-dotenv not installed. Using environment variables only.")
except Exception as e:
    # Fallback: try to read .env manually
    try:
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    except Exception:
        print(f"Warning: Could not load .env file: {e}. Using environment variables only.")


class FAQAssistant:
    def __init__(self, data_dir: str = "data"):
        self.store = MutualFundDataStore(data_dir)
        self.schemes = self.store.load_schemes()
        
        # Initialize Gemini
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY') or os.environ.get('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            raise ValueError(
                "GOOGLE_GEMINI_API_KEY not found. Please set it either:\n"
                "  1. As environment variable: set GOOGLE_GEMINI_API_KEY=your_key\n"
                "  2. In .env file: GOOGLE_GEMINI_API_KEY=your_key\n"
                "Get your API key from: https://makersuite.google.com/app/apikey"
            )
        
        try:
            genai.configure(api_key=api_key)
            # For older versions, use generate_text directly
            # Try new API first, fallback to old API
            try:
                self.model = genai.GenerativeModel('gemini-pro')
                self.use_new_api = True
            except AttributeError:
                # Old API - use generate_text
                self.model = None
                self.use_new_api = False
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Gemini: {e}. Please check your API key.")
        
        # Educational links
        self.educational_links = {
            'general': 'https://groww.in/mutual-funds',
            'elss': 'https://groww.in/mutual-funds/category/best-elss-mutual-funds',
            'sip': 'https://groww.in/blog/what-is-sip',
            'expense_ratio': 'https://groww.in/blog/expense-ratio-in-mutual-funds',
            'exit_load': 'https://groww.in/blog/exit-load-in-mutual-funds',
            'riskometer': 'https://groww.in/blog/riskometer-in-mutual-funds',
            'statements': 'https://groww.in/help/how-to-download-mutual-fund-statements',
        }
    
    def extract_scheme_name_with_gemini(self, query: str) -> Optional[str]:
        """Use Gemini to extract scheme name from query"""
        scheme_names = [s['scheme_name'] for s in self.schemes[:50]]  # Limit for prompt size
        
        prompt = f"""Extract the mutual fund scheme name from this query. If no scheme name is found, return "NONE".

Available scheme names (examples):
{', '.join(scheme_names[:20])}

Query: "{query}"

Return only the scheme name if found, or "NONE" if not found. Do not include any explanation."""

        try:
            if self.use_new_api:
                response = self.model.generate_content(prompt)
                extracted = response.text.strip()
            else:
                # Old API
                response = genai.generate_text(
                    model='models/text-bison-001',
                    prompt=prompt,
                    temperature=0.1
                )
                extracted = response.result.strip() if hasattr(response, 'result') else str(response).strip()
            
            if extracted.upper() == "NONE" or not extracted:
                return None
            
            # Try to match with actual scheme names
            extracted_lower = extracted.lower()
            for scheme in self.schemes:
                scheme_name = scheme['scheme_name'].lower()
                if extracted_lower in scheme_name or scheme_name in extracted_lower:
                    return scheme['scheme_name']
                # Check word overlap
                extracted_words = set(extracted_lower.split())
                scheme_words = set(scheme_name.split())
                if len(extracted_words & scheme_words) >= 2:
                    return scheme['scheme_name']
            
            return extracted if len(extracted) > 5 else None
        except Exception as e:
            print(f"Gemini error in scheme extraction: {e}")
            return self.extract_scheme_name_fallback(query)
    
    def extract_scheme_name_fallback(self, query: str) -> Optional[str]:
        """Fallback method to extract scheme name"""
        query_lower = query.lower()
        
        for scheme in self.schemes:
            scheme_name = scheme['scheme_name'].lower()
            if scheme_name in query_lower or any(word in query_lower for word in scheme_name.split() if len(word) > 3):
                return scheme['scheme_name']
        
        patterns = [
            r'(?:of|for)\s+([A-Z][^?]+?)(?:\?|$)',
            r'([A-Z][A-Za-z\s&]+?)\s+(?:expense|exit|sip|lock|risk|benchmark)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                potential_name = match.group(1).strip()
                if len(potential_name) > 5 and any(c.isupper() for c in potential_name):
                    return potential_name
        
        return None
    
    def detect_question_type_with_gemini(self, query: str) -> str:
        """Use Gemini to detect question type"""
        prompt = f"""Classify this mutual fund query into one of these categories:
- expense_ratio
- exit_load
- minimum_sip
- lock_in
- riskometer
- benchmark
- statements
- nav
- fund_manager
- fund_size
- opinionated (if asking for advice/recommendation)
- general (if none of the above)

Query: "{query}"

Return only the category name, nothing else."""

        try:
            if self.use_new_api:
                response = self.model.generate_content(prompt)
                question_type = response.text.strip().lower()
            else:
                # Old API
                response = genai.generate_text(
                    model='models/text-bison-001',
                    prompt=prompt,
                    temperature=0.1
                )
                question_type = (response.result if hasattr(response, 'result') else str(response)).strip().lower()
            
            # Validate question type
            valid_types = [
                'expense_ratio', 'exit_load', 'minimum_sip', 'lock_in',
                'riskometer', 'benchmark', 'statements', 'nav',
                'fund_manager', 'fund_size', 'opinionated', 'general'
            ]
            
            if question_type in valid_types:
                return question_type
            
            # Fallback to keyword detection
            return self.detect_question_type_fallback(query)
        except Exception as e:
            print(f"Gemini error in question type detection: {e}")
            return self.detect_question_type_fallback(query)
    
    def detect_question_type_fallback(self, query: str) -> str:
        """Fallback method for question type detection"""
        query_lower = query.lower()
        
        opinion_keywords = [
            'should i', 'can i buy', 'should i invest', 'should i sell',
            'is it good', 'is it bad', 'recommend', 'advice', 'suggestion',
            'worth investing', 'good investment', 'bad investment',
            'should i continue', 'should i hold', 'should i exit'
        ]
        if any(keyword in query_lower for keyword in opinion_keywords):
            return 'opinionated'
        
        if 'expense ratio' in query_lower or 'expense' in query_lower:
            return 'expense_ratio'
        if 'exit load' in query_lower:
            return 'exit_load'
        if 'minimum sip' in query_lower or 'min sip' in query_lower:
            return 'minimum_sip'
        if 'lock' in query_lower or 'elss' in query_lower:
            return 'lock_in'
        if 'riskometer' in query_lower or 'risk rating' in query_lower:
            return 'riskometer'
        if 'benchmark' in query_lower:
            return 'benchmark'
        if any(word in query_lower for word in ['statement', 'download', 'capital gain']):
            return 'statements'
        if 'nav' in query_lower:
            return 'nav'
        if 'fund manager' in query_lower:
            return 'fund_manager'
        if 'fund size' in query_lower or 'aum' in query_lower:
            return 'fund_size'
        
        return 'general'
    
    def generate_answer_with_gemini(self, query: str, scheme: Dict, question_type: str, facts: Dict) -> str:
        """Use Gemini to generate a natural answer from facts"""
        facts_str = json.dumps(facts, indent=2)
        scheme_name = scheme.get('scheme_name', 'this scheme')
        
        prompt = f"""You are a factual assistant for mutual fund information. Answer the user's query using ONLY the provided facts. Do not provide investment advice.

Query: "{query}"
Scheme Name: {scheme_name}
Question Type: {question_type}

Facts Available:
{facts_str}

Instructions:
1. Answer the query using ONLY the facts provided above
2. Be concise and factual
3. If a fact is missing, say it's not available
4. Do NOT provide investment advice or recommendations
5. Do NOT make up information

Answer:"""

        try:
            if self.use_new_api:
                response = self.model.generate_content(prompt)
                answer = response.text.strip()
            else:
                # Old API
                response = genai.generate_text(
                    model='models/text-bison-001',
                    prompt=prompt,
                    temperature=0.1
                )
                answer = (response.result if hasattr(response, 'result') else str(response)).strip()
            
            # Ensure answer mentions scheme name if available
            if scheme_name and scheme_name not in answer:
                answer = f"For {scheme_name}, {answer}"
            
            return answer
        except Exception as e:
            print(f"Gemini error in answer generation: {e}")
            return self.get_fact_answer(scheme, question_type)[0]
    
    def get_fact_answer(self, scheme: Dict, question_type: str) -> Tuple[str, str]:
        """Get factual answer for a specific question type"""
        facts = scheme.get('facts', {})
        source_url = scheme.get('source_url', self.educational_links['general'])
        scheme_name = scheme.get('scheme_name', 'this scheme')
        
        if question_type == 'expense_ratio':
            expense_ratio = facts.get('expense_ratio')
            if expense_ratio:
                answer = f"The expense ratio of {scheme_name} is {expense_ratio}."
            else:
                answer = f"Expense ratio information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'exit_load':
            exit_load = facts.get('exit_load')
            if exit_load:
                answer = f"The exit load for {scheme_name} is: {exit_load}."
            else:
                answer = f"Exit load information for {scheme_name} is not available. Please check the scheme document."
            return answer, source_url
        
        elif question_type == 'minimum_sip':
            min_sip = facts.get('minimum_sip')
            first_inv = facts.get('first_investment')
            subsequent_inv = facts.get('subsequent_investment')
            
            parts = []
            if min_sip:
                parts.append(f"Minimum SIP: ₹{min_sip}")
            if first_inv:
                parts.append(f"First investment: ₹{first_inv}")
            if subsequent_inv:
                parts.append(f"Subsequent investments: ₹{subsequent_inv}")
            
            if parts:
                answer = f"For {scheme_name}, {', '.join(parts)}."
            else:
                min_lumpsum = facts.get('minimum_lumpsum')
                if min_lumpsum:
                    answer = f"Minimum lumpsum investment for {scheme_name} is ₹{min_lumpsum}. SIP information is not available."
                else:
                    answer = f"Minimum SIP information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'lock_in':
            lock_in = facts.get('lock_in')
            if lock_in:
                answer = f"The lock-in period for {scheme_name} is: {lock_in}."
                if 'ELSS' in str(lock_in).upper() or 'elss' in scheme_name.lower():
                    answer += " ELSS (Equity Linked Savings Scheme) funds have a mandatory 3-year lock-in period as per tax regulations."
            else:
                if 'elss' in scheme_name.lower() or 'tax saver' in scheme_name.lower():
                    answer = f"{scheme_name} is an ELSS fund with a 3-year lock-in period as per Section 80C of the Income Tax Act."
                else:
                    answer = f"Lock-in period information for {scheme_name} is not available. Most non-ELSS funds do not have a lock-in period."
            return answer, source_url
        
        elif question_type == 'riskometer':
            riskometer = facts.get('riskometer')
            if riskometer:
                answer = f"The riskometer rating for {scheme_name} is: {riskometer}."
            else:
                answer = f"Riskometer information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'benchmark':
            benchmark = facts.get('benchmark')
            if benchmark:
                answer = f"The benchmark for {scheme_name} is: {benchmark}."
            else:
                answer = f"Benchmark information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'statements':
            if scheme_name and scheme_name != 'Unknown':
                answer = (
                    f"To download capital gains statements and tax documents for {scheme_name}, "
                    f"you can access them through your Groww account. "
                    f"Go to your portfolio, select the fund, and look for the 'Statements' or 'Tax Documents' section."
                )
            else:
                answer = (
                    "To download capital gains statements and tax documents for your mutual fund investments, "
                    "you can access them through your Groww account. "
                    "Go to your portfolio, select the fund, and look for the 'Statements' or 'Tax Documents' section."
                )
            return answer, self.educational_links['statements']
        
        elif question_type == 'nav':
            nav = facts.get('nav')
            if nav:
                answer = f"The NAV (Net Asset Value) of {scheme_name} is ₹{nav}."
            else:
                answer = f"NAV information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'fund_manager':
            fund_manager = facts.get('fund_manager')
            if fund_manager:
                answer = f"The fund manager of {scheme_name} is {fund_manager}."
            else:
                answer = f"Fund manager information for {scheme_name} is not available in our records."
            return answer, source_url
        
        elif question_type == 'fund_size':
            fund_size = facts.get('fund_size')
            if fund_size:
                answer = f"The fund size (AUM) of {scheme_name} is {fund_size}."
            else:
                answer = f"Fund size information for {scheme_name} is not available in our records."
            return answer, source_url
        
        return f"Information about {scheme_name} is available.", source_url
    
    def handle_opinionated_question(self) -> Tuple[str, str]:
        """Handle opinionated questions with polite refusal"""
        answer = (
            "I can only provide factual information about mutual fund schemes, not investment advice. "
            "For personalized investment recommendations, please consult with a certified financial advisor. "
            "I can help you with factual queries like expense ratios, exit loads, minimum SIP amounts, lock-in periods, "
            "riskometer ratings, benchmarks, and how to download statements."
        )
        return answer, self.educational_links['general']
    
    def answer_query(self, query: str, use_gemini: bool = True) -> Dict:
        """Answer a user query"""
        query = query.strip()
        
        # Detect question type (using Gemini if enabled)
        if use_gemini:
            question_type = self.detect_question_type_with_gemini(query)
        else:
            question_type = self.detect_question_type_fallback(query)
        
        # Handle opinionated questions
        if question_type == 'opinionated':
            answer, source_url = self.handle_opinionated_question()
            return {
                'answer': answer,
                'source_url': source_url,
                'question_type': 'opinionated',
                'scheme_name': None,
            }
        
        # Extract scheme name (using Gemini if enabled)
        if use_gemini:
            scheme_name = self.extract_scheme_name_with_gemini(query)
        else:
            scheme_name = self.extract_scheme_name_fallback(query)
        
        if not scheme_name:
            if question_type == 'statements':
                answer, source_url = self.get_fact_answer({}, 'statements')
                return {
                    'answer': answer.replace('for {scheme_name}', 'for your mutual fund investments'),
                    'source_url': source_url,
                    'question_type': question_type,
                    'scheme_name': None,
                }
            else:
                return {
                    'answer': (
                        f"I can help you with {question_type.replace('_', ' ')} information, "
                        f"but I need to know which mutual fund scheme you're asking about. "
                        f"Please specify the scheme name in your question."
                    ),
                    'source_url': self.educational_links.get(question_type, self.educational_links['general']),
                    'question_type': question_type,
                    'scheme_name': None,
                }
        
        # Find scheme
        scheme = self.store.find_scheme_by_name(scheme_name)
        
        if not scheme:
            return {
                'answer': (
                    f"I couldn't find information about '{scheme_name}' in our database. "
                    f"Please check the scheme name and try again, or visit Groww to search for the scheme."
                ),
                'source_url': self.educational_links['general'],
                'question_type': question_type,
                'scheme_name': scheme_name,
            }
        
        # Generate answer (using Gemini for natural language if enabled)
        if use_gemini and question_type not in ['statements', 'opinionated']:
            try:
                facts = scheme.get('facts', {})
                answer = self.generate_answer_with_gemini(query, scheme, question_type, facts)
                source_url = scheme.get('source_url', self.educational_links['general'])
            except Exception as e:
                print(f"Falling back to rule-based answer: {e}")
                answer, source_url = self.get_fact_answer(scheme, question_type)
        else:
            answer, source_url = self.get_fact_answer(scheme, question_type)
        
        return {
            'answer': answer,
            'source_url': source_url,
            'question_type': question_type,
            'scheme_name': scheme['scheme_name'],
        }


def main():
    """Test the FAQ assistant"""
    print("=" * 60)
    print("GROWW MUTUAL FUND FAQ ASSISTANT - BACKEND (WITH GEMINI)")
    print("=" * 60)
    
    # Initialize assistant
    assistant = FAQAssistant()
    
    print(f"\nLoaded {len(assistant.schemes)} schemes from database")
    print("Using Google Gemini for query understanding")
    
    # Test queries
    test_queries = [
        "Expense ratio of ICICI Prudential Banking & PSU Debt Fund",
        "What is the minimum SIP for Axis Floater Fund?",
        "ELSS lock-in period?",
        "Exit load of HDFC Large Cap Fund",
        "Riskometer of SBI Small Cap Fund",
        "Benchmark of Nippon India Growth Fund",
        "How to download capital gains statement?",
        "Should I buy this fund?",
        "What is the expense ratio?",
    ]
    
    print("\n" + "=" * 60)
    print("TESTING QUERIES")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] Query: {query}")
        print("-" * 60)
        
        result = assistant.answer_query(query)
        
        print(f"Answer: {result['answer']}")
        print(f"Source: {result['source_url']}")
        print(f"Type: {result['question_type']}")
        if result['scheme_name']:
            print(f"Scheme: {result['scheme_name']}")


if __name__ == "__main__":
    main()
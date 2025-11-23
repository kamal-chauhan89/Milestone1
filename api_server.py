"""
Simple API Server for FAQ Assistant
Provides REST API endpoint for answering queries
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from faq_assistant_backend import FAQAssistant
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)  # Enable CORS for frontend integration

# Initialize FAQ assistant
assistant = FAQAssistant()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'schemes_loaded': len(assistant.schemes)
    })

@app.route('/query', methods=['POST'])
def query():
    """Answer a user query"""
    try:
        data = request.get_json()
        query_text = data.get('query', '').strip()
        
        if not query_text:
            return jsonify({
                'error': 'Query is required'
            }), 400
        
        # Get answer
        result = assistant.answer_query(query_text)
        
        return jsonify({
            'success': True,
            'query': query_text,
            'answer': result['answer'],
            'source_url': result['source_url'],
            'question_type': result['question_type'],
            'scheme_name': result.get('scheme_name'),
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/schemes', methods=['GET'])
def list_schemes():
    """List all available schemes"""
    try:
        schemes = [{
            'id': s['id'],
            'name': s['scheme_name'],
            'category': s.get('category'),
        } for s in assistant.schemes[:100]]  # Limit to first 100
        
        return jsonify({
            'success': True,
            'total': len(assistant.schemes),
            'schemes': schemes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("FAQ ASSISTANT API SERVER")
    print("=" * 60)
    print(f"\nLoaded {len(assistant.schemes)} schemes")
    print("\nStarting server on http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /query - Answer a query")
    print("  GET /schemes - List available schemes")
    print("  GET /health - Health check")
    print("\nExample query:")
    print('  curl -X POST http://localhost:5000/query \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"query": "Expense ratio of ICICI Prudential Banking & PSU Debt Fund"}\'')
    print("\n" + "=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)


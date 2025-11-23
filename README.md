# Groww Mutual Funds FAQ Chatbot

An intelligent FAQ chatbot for Groww mutual funds that provides accurate, factual information about mutual fund schemes using AI-powered natural language understanding.

## Overview

This chatbot helps users get instant answers to questions about mutual funds, including expense ratios, exit loads, minimum SIP amounts, lock-in periods, risk levels, portfolio composition, and more. It uses Retrieval-Augmented Generation (RAG) to provide accurate, data-driven responses.

## Features

- **Conversational Interface**: Clean, modern chat UI with Groww branding
- **Context-Aware**: Remembers the fund being discussed across multiple questions
- **Comprehensive Information**: Access to 373+ mutual fund schemes data
- **Factual Responses**: Provides only verified information, no investment advice
- **Multiple Query Types**: Supports expense ratio, exit load, SIP amounts, risk ratings, portfolio composition, and more

## Technology Stack

### Backend
- **Python Flask**: RESTful API server
- **Google Gemini AI**: Advanced language model for natural language understanding
- **RAG (Retrieval-Augmented Generation)**: Combines information retrieval from database with AI generation
  - Retrieves specific fund data from scraped mutual fund information
  - Uses AI to generate natural, contextual responses based on retrieved facts
  - Ensures accuracy by grounding responses in actual data

### Frontend
- **HTML/CSS/JavaScript**: Responsive, mobile-first design
- **Gradient UI**: Purple/blue Groww-branded interface
- **Real-time Updates**: Typing indicators and smooth animations

### Data Pipeline
- **Web Scraping**: Automated data collection from Groww website
- **JSON Storage**: Structured fund information database
- **BeautifulSoup & Selenium**: For extracting fund details

## RAG Architecture

1. **Retrieval Phase**: User query is analyzed to identify the fund and question type
2. **Data Fetching**: Relevant fund facts are retrieved from the database
3. **Generation Phase**: Google Gemini AI generates a natural response using the retrieved facts
4. **Response**: User receives accurate, contextual information

## Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key in `.env`:
```
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

3. Start the backend server:
```bash
python api_server.py
```

4. Open the chatbot:
```bash
start chatbot.html
```

The API server will run on `http://localhost:5000` and the chatbot will connect automatically.

## Usage Examples

- "What is the expense ratio of ICICI Prudential Banking & PSU Debt Fund?"
- "Tell me about the exit load for SBI Bluechip Fund"
- "What's the minimum SIP amount for Axis Small Cap Fund?"
- "What is the risk level?" (after mentioning a fund)
- "Show me the portfolio composition"

## API Endpoints

- `POST /query`: Submit a question and get an answer
- `GET /schemes`: List available mutual fund schemes
- `GET /health`: Check API server status

## Project Structure

- `chatbot.html`: Frontend chat interface
- `api_server.py`: Flask API server
- `faq_assistant_backend.py`: Core chatbot logic with RAG implementation
- `data_storage.py`: Database operations
- `groww_scraper.py`: Web scraping scripts
- `requirements.txt`: Python dependencies

## Note

This chatbot provides factual information only and does not offer investment advice. For personalized investment recommendations, please consult a certified financial advisor.

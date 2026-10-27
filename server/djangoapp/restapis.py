import os
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Backend service URLs (Microservices if deployed or fallback)
backend_url = os.environ.get('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.environ.get('sentiment_analyzer_url', default="http://localhost:5050/")

POSITIVE_WORDS = {
    'fantastic', 'great', 'excellent', 'amazing', 'good', 'outstanding', 
    'superb', 'wonderful', 'terrific', 'love', 'best', 'pleased', 
    'helpful', 'friendly', 'courteous', 'recommend', 'seamless', 'transparent'
}

NEGATIVE_WORDS = {
    'bad', 'poor', 'terrible', 'horrible', 'awful', 'worst', 'disappointed', 
    'rude', 'scam', 'fraud', 'cheat', 'unacceptable', 'delayed', 'broken'
}

def analyze_review_sentiments(text):
    """
    Analyze the sentiment of a review text.
    If an external IBM Watson / microservice sentiment analyzer URL is active and reachable,
    it queries it; otherwise, it utilizes a documented local rule-based NLP fallback analyzer.
    """
    if not text:
        return "neutral"

    # Check external microservice if enabled
    if os.environ.get('ENABLE_EXTERNAL_SENTIMENT', 'false').lower() == 'true':
        url = f"{sentiment_analyzer_url}text={requests.utils.quote(text)}"
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                result = response.json()
                return result.get("sentiment", "neutral")
        except Exception as err:
            logger.info(f"External sentiment service offline ({err}); using local sentiment fallback.")

    # Local NLP sentiment fallback
    words = text.lower().split()
    pos_count = sum(1 for w in words if w.strip(".,!?:;'\"") in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w.strip(".,!?:;'\"") in NEGATIVE_WORDS)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def get_request(endpoint, **kwargs):
    """
    Generic GET request helper to query microservice endpoints.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}{endpoint}?{params}".rstrip("&")

    try:
        response = requests.get(request_url, timeout=5)
        return response.json()
    except Exception as err:
        logger.error(f"Network error in get_request: {err}")
        return None

def post_review(data_dict):
    """
    Generic POST request helper to submit a review to backend microservices.
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=5)
        return response.json()
    except Exception as err:
        logger.error(f"Network error in post_review: {err}")
        return None

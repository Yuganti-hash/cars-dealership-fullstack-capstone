import os
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments

logger = logging.getLogger(__name__)

# Paths to data storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALERS_FILE = os.path.join(BASE_DIR, 'database', 'data', 'dealerships.json')
REVIEWS_FILE = os.path.join(BASE_DIR, 'database', 'data', 'reviews.json')

def _load_dealers():
    if os.path.exists(DEALERS_FILE):
        with open(DEALERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('dealerships', [])
    return []

def _load_reviews():
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('reviews', [])
    return []

def _save_reviews(reviews_list):
    os.makedirs(os.path.dirname(REVIEWS_FILE), exist_ok=True)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'reviews': reviews_list}, f, indent=2)


@csrf_exempt
def login_user(request):
    """
    Authenticate user with username and password.
    Task 5 endpoint: /djangoapp/login
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"userName": username, "status": "Failed", "error": "Invalid username or password"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "Failed"}, status=400)
    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)


@csrf_exempt
def logout_request(request):
    """
    Log out the current authenticated user.
    Task 6 endpoint: /djangoapp/logout
    """
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


@csrf_exempt
def registration(request):
    """
    Register a new user account.
    Task 7 endpoint: /djangoapp/register
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            if not username or not password:
                return JsonResponse({"error": "Username and password are required.", "status": "Failed"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "Failed"}, status=400)
    return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)


def get_cars(request):
    """
    Retrieve all car makes and associated car models.
    Task 14 and 15 endpoint: /djangoapp/get_cars
    """
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
            "Type": car_model.type,
            "Year": car_model.year,
            "Dealer_ID": car_model.dealer_id,
        })
    return JsonResponse({"status": 200, "CarModels": cars})


def get_dealerships(request, state="all"):
    """
    Retrieve all dealerships or filter by state (supports Kansas/KS).
    Task 9 (All dealers) endpoint: /djangoapp/get_dealers
    Task 11 (Kansas dealers) endpoint: /djangoapp/get_dealers/Kansas or /djangoapp/get_dealers?state=Kansas
    """
    query_state = request.GET.get('state', state)
    all_dealers = _load_dealers()

    if query_state and query_state.lower() != "all":
        target = query_state.strip().lower()
        filtered = [
            d for d in all_dealers 
            if d.get("state", "").strip().lower() == target or d.get("st", "").strip().lower() == target
        ]
        return JsonResponse({"status": 200, "dealers": filtered})

    return JsonResponse({"status": 200, "dealers": all_dealers})


def get_dealer_details(request, dealer_id):
    """
    Retrieve single dealership details by dealer ID.
    Task 10 endpoint: /djangoapp/dealer/<dealer_id>
    """
    try:
        did = int(dealer_id)
    except ValueError:
        return JsonResponse({"status": 400, "error": "Invalid dealer ID"}, status=400)

    dealers = _load_dealers()
    for d in dealers:
        if d.get("id") == did:
            return JsonResponse({"status": 200, "dealer": [d]})

    return JsonResponse({"status": 404, "error": "Dealer not found"}, status=404)


def get_dealer_reviews(request, dealer_id):
    """
    Retrieve customer reviews for a given dealer ID with sentiment.
    Task 8 endpoint: /djangoapp/get_reviews/<dealer_id>
    """
    try:
        did = int(dealer_id)
    except ValueError:
        return JsonResponse({"status": 400, "error": "Invalid dealer ID"}, status=400)

    all_reviews = _load_reviews()
    dealer_reviews = []
    for r in all_reviews:
        if r.get("dealership") == did:
            # Check or evaluate sentiment
            if "sentiment" not in r or not r["sentiment"]:
                r["sentiment"] = analyze_review_sentiments(r.get("review", ""))
            dealer_reviews.append(r)

    return JsonResponse({"status": 200, "reviews": dealer_reviews})


@csrf_exempt
def add_review(request):
    """
    Submit a review for a dealership.
    Endpoint: /djangoapp/add_review
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            reviews = _load_reviews()
            new_id = max([r.get("id", 0) for r in reviews], default=0) + 1
            
            review_text = data.get("review", "")
            sentiment = analyze_review_sentiments(review_text)

            new_review = {
                "id": new_id,
                "dealership": int(data.get("dealership", 1)),
                "name": data.get("name") or (request.user.username if request.user.is_authenticated else "Customer"),
                "review": review_text,
                "purchase": data.get("purchase", False),
                "purchase_date": data.get("purchase_date", ""),
                "car_make": data.get("car_make", ""),
                "car_model": data.get("car_model", ""),
                "car_year": data.get("car_year", 2024),
                "sentiment": sentiment,
            }
            reviews.append(new_review)
            _save_reviews(reviews)
            return JsonResponse({"status": 200, "message": "Review added successfully", "review": new_review})
        except Exception as e:
            return JsonResponse({"status": 400, "error": str(e)}, status=400)
    return JsonResponse({"status": 405, "error": "Method not allowed"}, status=405)


def analyze_review(request, text=""):
    """
    Analyze sentiment of given text.
    Task 16 endpoint: /djangoapp/analyze/<text> or /djangoapp/analyze?text=...
    Tests exact text: 'Fantastic services' -> 'positive'
    """
    input_text = text or request.GET.get('text', '')
    if not input_text:
        return JsonResponse({"status": 400, "error": "Text parameter is required"}, status=400)
    
    sentiment = analyze_review_sentiments(input_text)
    return JsonResponse({
        "status": 200,
        "sentiment": sentiment,
        "text": input_text
    })

import requests
import json
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
import logging

logger = logging.getLogger(__name__)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "http://localhost:3030/fetchDealers"
    else:
        endpoint = "http://localhost:3030/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    endpoint = "http://localhost:3030/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail['review'])
        print(response)
        review_detail['sentiment'] = response['sentiment']
    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    endpoint = "http://localhost:3030/fetchDealer/" + str(dealer_id)
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception:
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"
    request_url = endpoint + params
    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception:
        print("Network exception occurred")


def post_review(data_dict):
    request_url = "http://localhost:3030/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception:
        print("Network exception occurred")


def analyze_review_sentiments(text):
    request_url = (
        "http://localhost:5000/analyze/" + text
    )
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print("Unexpected {}, {}".format(err, type(err)))
        return {"sentiment": "neutral"}


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        logger.debug("{} is a new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)
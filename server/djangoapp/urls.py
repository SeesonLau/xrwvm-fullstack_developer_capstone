from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_user, name='logout'),
    path(route='register', view=views.registration, name='register'),
    path(route='get_cars', view=views.get_cars, name='getcars'),
    path(
        route='get_dealerships',
        view=views.get_dealerships,
        name='get_dealerships'
    ),
    path(
        route='get_dealerships/<str:state>',
        view=views.get_dealerships,
        name='get_dealerships_by_state'
    ),
    path(
        route='dealer/<int:dealer_id>',
        view=views.get_dealer_details,
        name='dealer_details'
    ),
    path(
        route='reviews/dealer/<int:dealer_id>',
        view=views.get_dealer_reviews,
        name='dealer_reviews'
    ),
    path(route='add_review', view=views.add_review, name='add_review'),
]
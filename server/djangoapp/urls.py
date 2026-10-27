from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Authentication routes
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),

    # Car makes and models (Tasks 14 and 15)
    path('get_cars', views.get_cars, name='getcars'),

    # Dealership routes
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealers, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_details'),

    # Review routes
    path('get_reviews/<int:dealer_id>', views.get_dealer_reviews, name='get_reviews'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),

    # Sentiment analysis route
    path('analyze/<path:text>', views.analyze_review, name='analyze_review'),
    path('analyze', views.analyze_review, name='analyze_review_query'),
]

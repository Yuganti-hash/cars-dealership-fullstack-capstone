from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Coursera specific required microservice/proxy endpoints
    path('fetchDealers', app_views.get_dealers, name='fetch_dealers_root'),
    path('fetchDealers/<str:state>', app_views.get_dealers, name='fetch_dealers_by_state_root'),
    path('fetchDealer/<int:dealer_id>', app_views.get_dealer_by_id, name='fetch_dealer_by_id_root'),
    path('fetchReviews/dealer/<int:dealer_id>', app_views.get_dealer_reviews, name='fetch_reviews_by_dealer_root'),
    path('analyze/<path:text>', app_views.analyze_review, name='analyze_review_root'),
    path('analyze', app_views.analyze_review, name='analyze_review_query_root'),

    # Frontend routes
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),
    path('login/', TemplateView.as_view(template_name="index.html"), name='login_page'),
    path('register/', TemplateView.as_view(template_name="index.html"), name='register_page'),
    path('dealers/', TemplateView.as_view(template_name="index.html"), name='dealers_page'),
    path('dealer/<int:dealer_id>', TemplateView.as_view(template_name="index.html"), name='dealer_details_page'),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html"), name='post_review_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

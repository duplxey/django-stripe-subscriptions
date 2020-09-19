from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
]

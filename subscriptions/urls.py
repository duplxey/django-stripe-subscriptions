from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='subscriptions-home'),
    path('webhook/', views.stripe_webhook),
]
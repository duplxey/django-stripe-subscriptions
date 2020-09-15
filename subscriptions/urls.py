from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('webhook/', views.stripe_webhook),
]
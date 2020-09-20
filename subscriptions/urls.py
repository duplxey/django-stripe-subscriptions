from django.urls import path, include

from . import views
from .views import home_view, success_view, cancel_view

urlpatterns = [
    path('', home_view, name="subscriptions-home"),
    path('success/', success_view, name="subscriptions-success"),
    path('cancel/', cancel_view, name="subscriptions-cancel"),

    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),

    path('accounts/', include('allauth.urls')),
]

from django.urls import path

from .views import login_view, signup_view, logout_view

urlpatterns = [
    path('login/', login_view, name='customer-login'),
    path('signup/', signup_view, name='customer-signup'),
    path('logout/', logout_view, name='customer-logout'),
]
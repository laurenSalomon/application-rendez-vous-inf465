# urls.py

from django.urls import path
from .views import register, verify_otp,login

urlpatterns = [
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp'),
]

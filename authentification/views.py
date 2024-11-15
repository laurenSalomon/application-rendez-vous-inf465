# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser, OTP
from .forms import UserRegistrationForm, OTPVerificationForm
from django.conf import settings
from twilio.rest import Client
import random

def send_otp(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP code is {otp_code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            otp_code = random.randint(100000, 999999)
            OTP.objects.create(user=user, code=otp_code)
            send_otp(user.phone_number, otp_code)
            return redirect('verify_otp', user_id=user.id)
    else:
        form = UserRegistrationForm()
    return render(request, 'authentification/register.html', {'form': form})

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = OTP.objects.get(user=user, code=form.cleaned_data['code'])
            if otp and not otp.is_verified:
                otp.is_verified = True
                otp.save()
                login(request, user)
                return redirect('home')
    else:
        form = OTPVerificationForm()
    return render(request, 'authentification/verify_otp.html', {'form': form})

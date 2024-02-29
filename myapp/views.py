from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail




# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def register(request):
    print(request.method,'request.method')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(name=name, email=email, password=password)
        print(name,email,password)
        return redirect('login')
    
    else:        
        return render(request, 'register.html')
    
def login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(email=email, password=password)
        print(user,"user", email, password)
        if user is not None:
            auth_login(request, user)
            subject = 'Thank you for Signing Up '
            message = render_to_string('email_wlcm.html', {'user': user})
            from_email = 'sushilsingh5694@gmail.com'
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return render(request, 'index.html', {'error_message': email})
        else:  
            return render(request, 'login.html', {'error_message': 'Invalid Userame or Passward'})
    else:
        return render(request, 'login.html')
        
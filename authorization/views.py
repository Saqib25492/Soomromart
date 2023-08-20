from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from .utils import generate_token
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from itertools import chain

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')
        password1 = request.POST.get('password1')
        
        if password == password1:
            if User.objects.filter(username = username).exists():
                messages.warning(request, 'User Exists')
                return redirect('/auth/signup/')
            
            elif User.objects.filter(email = email).exists():
                messages.warning(request, 'Email Exist')
                return redirect('/auth/signup/')
                
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.is_active=False
                user.save()
                email_subject = "Activate your account"
                message = render_to_string('authentication/activate.html', {
                    'user':user,
                    'domain':'127.0.0.1:8000',
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user)
                })
                
                email_message = EmailMessage(
                    email_subject, 
                    message, 
                    settings.EMAIL_HOST_USER, 
                    [email])
                email_message.send()
                messages.success(request, 'Activate Your Account by clicking the link in your email')
                
                return redirect('/auth/login/')
        
        else:
            messages.warning(request, 'Password does not match')
            return redirect('/auth/signup/')
        
    return render(request, 'authentication/signup.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, 'Account Activated succesfully')
            return redirect('/auth/login/')

        return render(request, 'authentication/activatefail.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Username or Password is incorrect")
            return redirect('/auth/login/')
            
    return render(request, 'authentication/signin.html')

@login_required(login_url="/auth/login/")
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('/auth/login/')
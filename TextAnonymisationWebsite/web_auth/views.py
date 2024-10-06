from django.shortcuts import render

# Create your views here.
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm, EnterEmailForPasswordResetForm, ResetPasswordForm
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from .tokens import account_activation_token,password_reset_token
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("/finished_registration")
            elif user is not None and not user.is_active:
                messages.error(request, 'Please, confirm your email to activate your account.')
            else:
                messages.error(request, 'Invalid credentials. Try again.')
        else:
            messages.error(request, 'Error validating the login form')

    html_template = loader.get_template('website_auth/login_template.html')
    context = {'form': form,
               'link': reverse('website_auth:login'),
               'title': 'Login',
               'button': 'Login',
               'show_signup': True,
               'show_reset_password': True
               }
    return HttpResponse(html_template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect("website_auth:login")

def signup_view(request):
    msg = None
    success = False
    if settings.DEVELOPMENT:
        messages.error(request, 'Registration is not available in development mode')
        return redirect(reverse('website_auth:login'))

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email {email} is already in use. If you do not remeber your password, use password <a href={reverse("website_auth:reset_password")}> reset. </a>')
                return redirect(reverse('website_auth:signup'))

            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            user.is_active = False
            user.save()
            if user is not None:
                activateEmail(request, user, user.email)
                return redirect(reverse('website_auth:login'))
        else:
            messages.error(request, "Something went wrong. Please take a look on the registration form again.")
    else:
        form = SignUpForm()
    
    context = {'form': form,
            'link': reverse('website_auth:signup'),
            'title': 'Sign Up',
            'button': 'Sign Up'
    }

    return render(request, "website_auth/login_template.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid activation link')
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.error(request, 'Activation link is invalid!')             

    return redirect('website_auth:login')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('website_auth/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <i>Note</i>: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def send_reset_password_email(request, user, to_email):
    mail_subject = 'Reset your password.'
    message = render_to_string('website_auth/reset_password_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': password_reset_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    messages.info(request, f'If the e-mail provided exists, we will send you confirmation link to reset your password.')
    email = EmailMessage(mail_subject, message, to=[to_email])
    return email.send()

def reset_password_view(request):
    if request.method ==    "GET":
        form  = EnterEmailForPasswordResetForm()
    elif request.method == "POST":
        form = EnterEmailForPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = User.objects.get(email=email)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                messages.error(request, 'User with this email does not exist.')
                return redirect(reverse('website_auth:reset_password'))
            _ = send_reset_password_email(request, user, email)
            return redirect(reverse('website_auth:login'))
        
    context = { 'form': form,
                'link': reverse('website_auth:reset_password'),
                'title': 'Reset Password',
                'button': 'Reset',
                'show_signup': True}

    return render(request, "website_auth/login_template.html", context)

def reset_password_link_view(request, uidb64, token):
    this_url = reverse('website_auth:reset_password_link', kwargs={'uidb64': uidb64, 'token': token})
    if request.method == "GET":
        form = ResetPasswordForm()
        context = { 'form' : form,
                    'title': 'Reset Password via Link',
                    'button': 'Reset',
                    'link': this_url,
                  }
        return render(request, "website_auth/login_template.html", context=context)
    elif request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get("password1")
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                messages.error(request, 'Invalid activation link')
                
            if user is not None and password_reset_token.check_token(user, token):
                same_password = user.check_password(password1)
                if same_password:
                    messages.error(request, 'Entered password is the same as the old one.')
                    return redirect(this_url)
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect(reverse('website_auth:login'))
            else:
                messages.error(request, 'Password reset failed. Are you using the old password reset link?')
                return redirect(this_url)
        else:
            messages.error(request, 'Password reset failed')
            return redirect(this_url)
         
    return redirect('website_auth:login')
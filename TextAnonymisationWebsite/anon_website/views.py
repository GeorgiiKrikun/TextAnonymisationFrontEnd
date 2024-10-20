from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from anon_website.forms import LoginForm, SignupForm, TryForm
from django.conf import settings
from TextAnonymisationEngine.Engine.Lang import Lang

@login_required(login_url=reverse_lazy('web_auth:login'))
def anonymise_view(request):
    context = {'languages': []}
    for lang in Lang:
        context['languages'].append({"value" : lang.value, 
                                     "name" : lang.name})
    return render(request, 'anon_website/anonymise.html', context=context)

def try_view(request):
    form = TryForm()
    context = {'form': form,
               'api_token': settings.API_FREE_KEY}
    
    return render(request, 'anon_website/try.html', context=context)

def home_view(request):
    return render(request, 'anon_website/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('anonymise')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    context = {'form': form,
               'link': reverse('login'),
               'title': 'Login',
               'button': 'Login',
               'show_signup': True}
    return render(request, 'anon_website/login_template.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password != password_confirm:
                form.add_error(None, 'Passwords do not match')
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('login')
    elif request.method == 'GET':
        form = SignupForm()
            

    context = {'form': 'form',
                'link': reverse('signup'),
                'title': 'Sign Up',
                'button': 'Sign Up',
                'show_signup': False}
    return render(request, 'anon_website/login_template.html', context)

def finished_registration_view(request):
    return redirect(reverse('anon_website:home'))
